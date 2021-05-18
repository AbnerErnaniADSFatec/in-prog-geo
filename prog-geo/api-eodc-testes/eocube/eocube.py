"""
4. API - EO Data Cube.
"""

import datetime
import json

import requests
import stac
import wtss

from eocube import config


def _response(url, json_obj=False, obj={}):
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    if json_obj:
        return requests.post(url, data=json.dumps(obj), headers=headers).json()
    else:
        return requests.get(url).json()

class Image():

    def __init__(self, item, bands, bbox):
        self.item = item
        self.bands = bands
        self.bbox = bbox

    def getBand(self, band):
        return self.item.read(
            self.bands[band], bbox=self.bbox
        )

    # Função para cálculo do índice NDVI
    def _ndvi(self, nir, red, cte_delta=1e-10):
        ndvi = (nir - red) / (nir + red + cte_delta)
        return ndvi

    # Função para cálculo do índice NDWI
    def _ndwi(self, nir, green, cte_delta=1e-10):
        ndwi = (green - nir) / (green + nir + cte_delta)
        return ndwi

    # Função para cálculo do índice NDBI
    def _ndbi(self, nir, swir1, cte_delta=1e-10):
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
