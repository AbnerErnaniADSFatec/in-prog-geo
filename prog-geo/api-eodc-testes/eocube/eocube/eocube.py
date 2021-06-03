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

from .image import Image
from .utils import Utils

from eocube import config

warnings.filterwarnings("ignore")

class DataCube():
    """Abstraction to create earth observation data cubes using images collected by STAC.py.

    ## Methods

    getCollections(), getDescription(),
    getItems(), createCube(), getCubeByBand(), getCube()
    """

    def __init__(self, collections=[], query_bands=[], bbox=(), start_date=None, end_date=None, limit=30):
        """Get items by STAC url service.

        Create a data cube using images collected from STAC using Image abstration.

        Build DataCube object with config parameters including access token, STAC url and earth observation service url.

        ## Parameters

        ### collections : string list, required

            The list with name of collections selected by user.

        ### query_bands : string list, required

            The list with commom name of bands [].

        ### bbox : tupple, required

            The bounding box with user Area of Interest.

        ### start_date : string, required

            The string start date formated "yyyy-mm-dd" to complete the interval.

        ### end_date : string, required

            The string end date formated "yyyy-mm-dd" to complete the interval.

        ### limit : int, required

            The limit of response images.
        """
        if len(config.ACCESS_TOKEN) == 0:
            config.ACCESS_TOKEN = input("Please insert a valid user token from BDC Auth: ")

        if len(config.EOCUBE_URL) == 0:
            config.EOCUBE_URL = input("Please insert a valid url for EO Service: ")

        if len(config.STAC_URL) == 0:
            config.STAC_URL = input("Please insert a valid url for STAC Service: ")

        self.utils = Utils()

        self.stac_service = stac.STAC(
            config.STAC_URL,
            access_token=config.ACCESS_TOKEN
        )

        if not collections:
            raise AttributeError("Please insert a list of available collections!")
        else:
            self.collections = collections

        if not query_bands:
            raise AttributeError("Please insert a list of available bands with query_bands!")
        else:
            self.query_bands = query_bands

        if not bbox:
            raise AttributeError("Please insert a bounding box parameter!")
        else:
            valid = self.utils._validateBBOX(bbox)
            if valid:
                self.bbox = bbox

        try:
            _start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d')
            _end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d')
            if _end_date <= _start_date:
                raise ValueError("Start date is greatter than end date!")
            else:
                self.start_date = start_date
                self.end_date = end_date
        except:
            raise ValueError("Dates are not correctly formatted, should be %Y-%m-%d")

        self.query = None
        self.items = None
        self.images = []

        try:
            # arazenar a query globalmente para utilizar os parametros de bounding box
            # e data inicial e final
            self.query = {
                'collections': collections,
                'bbox': bbox,
                'datetime': f'{start_date}/{end_date}',
                'limit': limit
            }
            self.items = self.stac_service.search(self.query)
        except:
            raise RuntimeError("Connection refused!")

        if self.items:
            # Cria uma lista de objetos Images com os items no STAC
            for item in self.items.features:
                bands = {}
                available_bands = item.get('properties').get('eo:bands')
                for band in available_bands:
                    band_common_name = str(band.get('common_name'))
                    if band_common_name in query_bands:
                        # Cria um dicionário com cada chave sendo o nome comum da banda e o nome dado pelo item
                        bands[band_common_name] = band.get('name')
                    else:
                        pass
                self.images.append(
                    Image(
                        item=item,
                        bands=bands,
                        bbox=self.query['bbox']
                    )
                )

        # Verifica se o cubo de dados foi criado com sucesso
        if len(self.images) == 0:
            raise ValueError("No data cube created!")

        x_data = {}

        for image in self.getImages():
            date = datetime.datetime.strptime(
                image.item["properties"]["datetime"],
                '%Y-%m-%dT%H:%M:%S'
            )
            x_data[date] = []
            for band in query_bands:
                data = image.getBand(band)
                longitude = list(range(0, len(data[0])))
                latitude = list(range(0, len(data)))
                x_data[date].append({
                    str(band): data
                })

        timeline = sorted(list(x_data.keys()))
        data_timeline = {}

        for i in range(len(list(bands))):
            data_timeline[bands[i]] = []
            for time in timeline:
                data_timeline[bands[i]].append(
                    x_data[time][i][bands[i]]
                )

        time_series = []
        for band in bands:
            time_series.append(
                data_timeline[band]
            )

        self.data_array = xr.DataArray(
            np.array(time_series),
            coords=[bands, timeline, longitude, latitude],
            dims=["band", "time", "laitude", "latitude"]
        )

        self.data_array.attrs = self.getDescription()

    def getDataCube(self):
        """Return a xarray with available data cube."""
        return self.data_array

    def getImages(self):
        """Return a list with available images collected by STAC."""
        return self.images

    def getCollections(self):
        """Return a list with available collections from STAC."""
        try:
            return list(self.stac_service.collections.keys())
        except:
            return None

    def getDescription(self):
        """Return a description JSON by collection name from STAC.

        ## Parameters

        ### collection_name : string, required

            The collection name available on getCollections() list.
        """
        try:
            description = {}
            for collection in self.collections:
                response = self.stac_service.collections[collection]
                description[collection] = {
                    "id": response["id"],
                    "title": response["title"],
                    "descriptions": response["bdc:metadata"]["datacite"]["descriptions"],
                    "extent": response["extent"],
                    "properties": response["properties"]
                }
            return description
        except:
            return None
