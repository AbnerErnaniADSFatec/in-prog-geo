"""
4. API - EO Data Cube.
"""

import requests
import wtss
import stac

class EOCube():

    def __init__(self, url, num):
        self.url = url
        self.num = num

    def getRandoms(self):
        response = requests.get(self.url + '/' + str(self.num))
        return response.json()
