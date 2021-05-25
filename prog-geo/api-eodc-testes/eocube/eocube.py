"""
API - EO Data Cube.

Python Client Library for Earth Observation Data Cubes.
This abstraction uses STAC.py library provided by BDC Project.

=======================================
begin                : 2021-05-01
git sha              : $Format:%H$
copyright            : (C) 2020 by none
email                : none@inpe.br
=======================================

This program is free software.
You can redistribute it and/or modify it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or (at your option) any later version.
"""

import datetime
import json

import numpy as np
import requests
import stac
import wtss
from rasterio.windows import Window

from eocube import config


def _response(url, json_obj=False, obj=None):
    """Get response JSON from url using object.

    ## Parameters

    ### url : string, required

        The site or service url.

    ### json_obj : boolean, optional

        If there is a JSON object to POST (default is False).

    ### obj : dictionary, optional

        Request the JSON object for POST type, ignored if `json_obj` is False (default is None).

    ## Raise

    ### HttpErrors

        If the resquested url is not valid or not exist.
    """
    # Headers for request on POST by default
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    # Verify if json_obj exists by boolean key
    if json_obj:
        # Return the requested response from url
        return requests.post(url, data=json.dumps(obj), headers=headers).json()
    else:
        # Uses get if json_obj not exists
        return requests.get(url).json()

def _normalize(array):
    """Normalizes numpy arrays into scale 0.0 - 1.0.

    ## Parameters

    ### array : nparray, required

        The nparray multidimensional for normalize

    ## Raise

    ### ValueError

        If the resquested nparray is invalid or not typed.
    """
    # Using techniques from statistics for normalize
    array_min, array_max = array.min(), array.max()
    return ((array - array_min)/(array_max - array_min))

class Image():
    """Abstraction to rasters files collected by STAC.py.

    ## Parameters

    ### item : ItemCollection, required

        The ItemCollection from STAC Python Library.
        GeoJSON Feature Collection of STAC Items.

    ### bands : dictionary, required

        A python dictionary with bands real name
        referenced by key with commom name.

    ### bbox : tupple, required

        The bounding box value with longitude and latitude values.

    ## Methods

    getBand(), _ndvi(), _ndwi(), _ndbi(),
    getNDVI(), getNDWI(), getNDBI()
    """

    def __init__(self, item, bands, bbox):
        """Build the Image Object for collected items from STAC."""
        self.item = item
        self.bands = bands
        self.bbox = bbox

    def getBand(self, band, wd=None):
        """Get bands from STAC item using commom name for band.

        ## Parameters

        ### band : string, required

            The band commom name.

        ### wd : rasterio.Window, optional

            The window from rasterio abstration for crop images.

        ## Raise

        ### ValueError

            If the resquested key not exists.
        """
        if wd:
            return self.item.read(
                self.bands[band], window=wd
            )
        else:
            return self.item.read(
                self.bands[band], bbox=self.bbox
            )

    def _ndvi(self, nir, red, cte_delta=1e-10):
        """Calculate the Normalized Difference Vegetation Index - NDVI.

        ## Parameters

        ### nir : np.array, required

            A multidimensional nparray with next infrared values.

        ### red : np.arrary, required

            A multidimensional nparray with band red values.

        ### cte_delta : float, optional

            A float number to prevent zero values on formula.

        ## Raise

        ### ValueError

            If the resquested nparray is invalid or not typed.
        """
        # Função para cálculo do índice NDVI
        ndvi = (nir - red) / (nir + red + cte_delta)
        return ndvi

    def _ndwi(self, nir, green, cte_delta=1e-10):
        """Calculate the Normalized Difference Water Index - NDWI.

        ## Parameters

        ### nir : np.array, required

            A multidimensional nparray with next infrared values.

        ### green : np.arrary, required

            A multidimensional nparray with band green values.

        ### cte_delta : float, optional

            A float number to prevent zero values on formula.

        ## Raise

        ### ValueError

            If the resquested nparray is invalid or not typed.
        """
        # Função para cálculo do índice NDWI
        ndwi = (green - nir) / (green + nir + cte_delta)
        return ndwi

    # Função para cálculo do índice NDBI
    def _ndbi(self, nir, swir1, cte_delta=1e-10):
        """Calculate the Normalized Difference Water Index - NDWI.

        ## Parameters

        ### nir : np.array, required

            A multidimensional nparray with next infrared values.

        ### green : np.arrary, required

            A multidimensional nparray with band green values.

        ### cte_delta : float, optional

            A float number to prevent zero values on formula.

        ## Raise

        ### ValueError

            If the resquested nparray is invalid or not typed.
        """
        ndbi = (swir1 - nir) / (swir1 + nir + cte_delta)
        return ndbi

    def getNDVI(self):
        return self._ndvi(
            nir=self.getBand("nir"),
            red=self.getBand("red")
        )

    def getNDWI(self):
        self._ndwi(
            nir=self.getBand("nir"),
            green=self.getBand("green")
        )

    def getNDBI(self):
        self._ndbi(
            nir=self.getBand("nir"),
            swir1=self.getBand("swir1")
        )

    def getRGB(self):
        red = self.getBand("red", wd=Window(0, 0, 500, 500))
        green = self.getBand("green", wd=Window(0, 0, 500, 500))
        blue = self.getBand("blue", wd=Window(0, 0, 500, 500))
        return np.dstack(
            (
                _normalize(red),
                _normalize(green),
                _normalize(blue)
            )
        )

class DataCube():

    def __init__(self):
        if len(config.ACCESS_TOKEN) == 0:
            config.ACCESS_TOKEN = input("Please insert a valid user token from BDC Auth: ")
        if len(config.EOCUBE_URL) == 0:
            config.EOCUBE_URL = input("Please insert a valid url for EO Service: ")
        if len(config.STAC_URL) == 0:
            config.STAC_URL = input("Please insert a valid url for STAC Service: ")
        self.stac_service = stac.STAC(
            config.STAC_URL,
            access_token=config.ACCESS_TOKEN
        )
        self.query = None
        self.items = None
        self.images = []

    def getCollections(self):
        try:
            # response = _response(config.EOCUBE_URL + "/collections")
            # collections = response['collections']
            # return collections
            return list(self.stac_service.collections.keys())
        except:
            return []

    def getDescription(self, collection_name=""):
        try:
            # response = _response(
            #     config.EOCUBE_URL +
            #     f"/describe/{collection_name}?token={config.ACCESS_TOKEN}"
            # )
            response = self.stac_service.collections[collection_name]
            return {
                "id": response["id"],
                "title": response["title"],
                "descriptions": response["bdc:metadata"]["datacite"]["descriptions"],
                "extent": response["extent"],
                "properties": response["properties"]
            }
        except:
            return None

    def getItems(self, collections=[], bbox=(),
        start_date=None, end_date=None, limit=30):
        try:
            self.query = {
                'collections': collections,
                'bbox': bbox,
                'datetime': f'{start_date}/{end_date}',
                'limit': limit
            }
            # items = _response(
            #     url=config.EOCUBE_URL + f"/search?token={config.ACCESS_TOKEN}",
            #     json_obj=True,
            #     obj={
            #         "collections": collections,
            #         "bbox": bbox,
            #         "interval": [
            #             start_date,
            #             end_date
            #         ],
            #         "limit": limit
            #     }
            # )["result"]
            # return self.items
            self.items = self.stac_service.search(self.query)
            return self.items.features
        except:
            return None

    ## Só é possível com a biblioteca STAC.py
    def createCube(self):
        if self.items:
            for item in self.items.features:
                bands = {}
                for band in item.get('properties').get('eo:bands'):
                    bands[str(band.get('common_name'))] = band.get('name')
                self.images.append(
                    Image(
                        item=item,
                        bands=bands,
                        bbox=self.query['bbox']
                    )
                )
        if len(self.images) != 0:
            return True
        else:
            return False

    def getCube(self):
        return self.images
