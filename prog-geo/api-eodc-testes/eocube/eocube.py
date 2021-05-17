"""
4. API - EO Data Cube.
"""

import requests
import stac
import wtss

from eocube import config


def _response(url):
    return requests.get(url).json()

class Cube():

    def __init__(self, stac_service):
        self.name = "Hello"

    def _evi(self):
        return 0

    def _ndvi(self):
        return 0

    def _ndwi(self):
        return 0

    def _ndbi(self):
        return 0

class EOCube():

    def __init__(self):
        if len(config.ACCESS_TOKEN) == 0:
            config.ACCESS_TOKEN = input("Please insert a valid user token from BDC Auth: ")
        if len(config.EOCUBE_URL) == 0:
            config.EOCUBE_URL = input("Please insert a valid url for EO Service: ")

    def getRandomNumbers(self, number=10):
        return _response(
            config.EOCUBE_URL + f"/{str(number)}"
        )

    def getCollections(self):
        response = _response(
            config.EOCUBE_URL +
            f"/collections?token={config.ACCESS_TOKEN}"
        )
        collections = response['collections']
        return collections