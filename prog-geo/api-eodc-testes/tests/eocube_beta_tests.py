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

from eocube import config

warnings.filterwarnings("ignore")

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
