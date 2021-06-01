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
import warnings

import numpy as np
import rasterio
import requests
import stac
import wtss
import xarray as xr
from pyproj import CRS, Proj, transform
from rasterio.windows import Window

from eocube import config

warnings.filterwarnings("ignore")

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
    """Normalize numpy arrays into scale 0.0 - 1.0.

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

    listBands(), getBand(),
    _ndvi(), _ndwi(), _ndbi(),
    getNDVI(), getNDWI(), getNDBI(), getRGB(),
    _afim()
    """

    def __init__(self, item, bands, bbox):
        """Build the Image Object for collected items from STAC."""
        self.item = item
        self.bands = bands
        self.bbox = bbox

    def listBands(self):
        """Get a list with available bands commom name."""
        return list(self.bands.keys())

    def getBand(self, band, bbox=None, wd=None):
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

        if bbox:
            return self.item.read(
                self.bands[band], bbox=bbox
            )
        elif wd:
            return self.item.read(
                self.bands[band], window=wd
            )
        else:
            wd = Window(0, 0, 500, 500)
            return self.item.read(
                self.bands[band], window=wd
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

    def _ndbi(self, nir, swir1, cte_delta=1e-10):
        """Calculate the Normalized Difference Built-up Index - NDBI.

        ## Parameters

        ### nir : np.array, required

            A multidimensional nparray with next infrared values.

        ### swir1 : np.arrary, required

            A multidimensional nparray with band swir1 values.

        ### cte_delta : float, optional

            A float number to prevent zero values on formula.

        ## Raise

        ### ValueError

            If the resquested nparray is invalid or not typed.
        """
        # Função para cálculo do índice NDBI
        ndbi = (swir1 - nir) / (swir1 + nir + cte_delta)
        return ndbi

    def getNDVI(self):
        """Calculate the Normalized Difference Vegetation Index - NDVI by image colected values.

        ## Raise

        ### KeyError

            If the required band does not exist.
        """
        return self._ndvi(
            nir=self.getBand("nir"),
            red=self.getBand("red")
        )

    def getNDWI(self):
        """Calculate the Normalized Difference Water Index - NDWI by image colected values.

        ## Raise

        ### KeyError

            If the required band does not exist.
        """
        self._ndwi(
            nir=self.getBand("nir"),
            green=self.getBand("green")
        )

    def getNDBI(self):
        """Calculate the Normalized Difference Built-up Index - NDBI by image colected values.

        ## Raise

        ### KeyError

            If the required band does not exist.
        """
        self._ndbi(
            nir=self.getBand("nir"),
            swir1=self.getBand("swir1")
        )

    def getRGB(self):
        """Get thee RGB image with real color.

        ## Raise

        ### KeyError

            If the required band does not exist.
        """
        red = self.getBand("red")
        green = self.getBand("green")
        blue = self.getBand("blue")
        linhas = blue.shape[0]
        colunas = blue.shape[1]
        array_rgb = np.zeros((linhas, colunas, 3))
        array_rgb[:, :, 0] = red / red.max()
        array_rgb[:, :, 1] = green / green.max()
        array_rgb[:, :, 2] = blue / blue.max()
        return array_rgb

    def _afim(self, x, y, band):
        """Calculate the long lat of a given point from band matrix.

        ## Parameters

        ### x : int, required

            For colunms.

        ### y : int, required

            For lines.

        ### band : string, required

            An available band to create a dataset.

        ## Raise

        ### ValueError

            If the resquested coordinate is invalid or not typed.

        """
        link = self.item.assets[
            self.bands[band]
        ]['href']
        with rasterio.open(link) as dataset:
            coord = dataset.transform * (y, x)
            lon, lat = transform(
                dataset.crs.wkt,
                Proj(init=CRS.from_string("EPSG:4326")),
                coord[0], coord[1]
            )
        return (lon, lat)

class DataCube():
    """Abstraction to create earth observation data cubes using images collected by STAC.py.

    ## Methods

    getCollections(), getDescription(),
    getItems(), createCube(), getCubeByBand(), getCube()
    """

    def __init__(self):
        """Build DataCube object with config parameters including access token, STAC url and earth observation service url."""
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
        """Return a list with available collections from STAC."""
        try:
            # response = _response(config.EOCUBE_URL + "/collections")
            # collections = response['collections']
            # return collections
            return list(self.stac_service.collections.keys())
        except:
            return None

    def getDescription(self, collection_name):
        """Return a description JSON by collection name from STAC.

        ## Parameters

        ### collection_name : string, required

            The collection name available on getCollections() list.
        """
        try:
            # response = _response(
            #     config.EOCUBE_URL +
            #     f"/describe/{collection_name}?token={config.ACCESS_TOKEN}"
            # )
            response = self.stac_service.collections[collection_name]
            # Retorna uma resposta personalizada do STAC
            # Necessita da biblioteca instalada
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
        """Get items by STAC url service.

        ## Parameters

        ### collections : string list, required

            The list with name of collections selected by user.

        ### bbox : tupple, required

            The bounding box with user Area of Interest.

        ### start_date : string, required

            The string start date formated "yyyy-mm-dd" to complete the interval.

        ### end_date : string, required

            The string end date formated "yyyy-mm-dd" to complete the interval.
        """
        try:
            # arazenar a query globalmente para utilizar os parametros de bounding box
            # e data inicial e final
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
            # Retornando apenas as fetures para coletar as imagens
            return self.items.features
        except:
            return None


    def createCube(self):
        """Create a data cube using images collected from STAC using Image abstration."""
        ## Só é possível com a biblioteca STAC.py
        if self.items:
            # Cria uma lista de objetos Images com os items no STAC
            for item in self.items.features:
                bands = {}
                for band in item.get('properties').get('eo:bands'):
                    # Cria um dicionário com cada chave sendo o nome comum da banda e o nome dado pelo item
                    bands[str(band.get('common_name'))] = band.get('name')
                self.images.append(
                    Image(
                        item=item,
                        bands=bands,
                        bbox=self.query['bbox']
                    )
                )
        # Verifica se o cubo de dados foi criado com sucesso
        if len(self.images) != 0:
            return True
        else:
            return False

    def getCubeByBand(self, band):
        """Create a dataset with a given band in time.

        ## Parameters

        ### band : string, required

            An available band to create a dataset.
        """
        # loc["2000-01-01":"2000-01-02", "IA"]
        x_data = []
        time = []
        for image in self.getCube():
            date = datetime.datetime.strptime(
                image.item["properties"]["datetime"],
                '%Y-%m-%dT%H:%M:%S'
            )
            data = image.getBand(band)
            x_data.append(data)
            time.append(date)
        return xr.DataArray(
            np.array(x_data),
            coords=[time],
            dims=["time"]
        )

    def getCube(self):
        """Get the data cube created by createCube() method."""
        return self.images
