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
import requests
import stac
import wtss
import xarray as xr

from eocube import config

from .image import Image
from .utils import Utils

warnings.filterwarnings("ignore")


class EOCube():
    """Abstraction to create earth observation data cubes using images collected by STAC.py.
    Create a data cube using images collected from STAC using Image abstration.

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

    def __init__(self, collections=[], query_bands=[], bbox=(), start_date=None, end_date=None, limit=30):
        """Build DataCube object with config parameters including access token, STAC url and earth observation service url."""

        if len(config.ACCESS_TOKEN) == 0:
            config.ACCESS_TOKEN = input("Please insert a valid user token from BDC Auth: ")

        if len(config.EOCUBE_URL) == 0:
            config.EOCUBE_URL = input("Please insert a valid url for EO Service: ")

        if len(config.STAC_URL) == 0:
            config.STAC_URL = input("Please insert a valid url for STAC Service: ")

        self.utils = Utils()

        self.stac_client = stac.STAC(
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
            self.query_bands = [band.lower() for band in query_bands]

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
                raise ValueError("Start date is greater than end date!")
            else:
                self.start_date = start_date
                self.end_date = end_date
        except:
            raise AttributeError("Dates are not correctly formatted, should be %Y-%m-%d")

        self.timeline = []
        self.data_images = {}
        self.data_array = None

        items = None
        try:
            # arazenar a query globalmente para utilizar os parametros de bounding box
            # e data inicial e final
            items = self.stac_client.search({
                'collections': self.collections,
                'bbox': self.bbox,
                'datetime': f'{self.start_date}/{self.end_date}',
                'limit': limit
            })
        except:
            raise RuntimeError("Connection refused!")

        images = []
        if items:
            # Cria uma lista de objetos Images com os items no STAC
            for item in items.features:
                bands = {}
                available_bands = item.get('properties').get('eo:bands')
                for band in available_bands:
                    band_common_name = str(band.get('common_name'))
                    if band_common_name in self.query_bands:
                        # Cria um dicionário com cada chave sendo o nome comum da banda e o nome dado pelo item
                        bands[band_common_name] = band.get('name')
                    else:
                        pass
                images.append(
                    Image(
                        item=item,
                        bands=bands,
                        bbox=self.bbox
                    )
                )

        # Verifica se o cubo de dados foi criado com sucesso
        if len(images) == 0:
            raise ValueError("No data cube created!")

        x_data = {}
        for image in images:
            date = image.time
            self.data_images[date] = image
            x_data[date] = []
            for band in self.query_bands:
                data = image.getBand(band)
                x = list(range(0, len(data[0])))
                y = list(range(0, len(data)))
                x_data[date].append({
                    str(band): data
                })

        self.timeline = sorted(list(x_data.keys()))

        data_timeline = {}
        for i in range(len(list(self.query_bands))):
            data_timeline[self.query_bands[i]] = []
            for time in self.timeline:
                data_timeline[self.query_bands[i]].append(
                    x_data[time][i][self.query_bands[i]]
                )

        time_series = []
        for band in self.query_bands:
            time_series.append(
                data_timeline[band]
            )

        self.data_array = xr.DataArray(
            np.array(time_series),
            coords=[self.query_bands, self.timeline, y, x],
            dims=["band", "time", "y", "x"],
            name=["DataCube"]
        )
        self.data_array.attrs = self.getDescription()

    def getDescription(self):
        """Return a description JSON by collection name from STAC.

        ## Parameters

        ### collection_name : string, required

            The collection name available on getCollections() list.
        """
        try:
            description = {}
            for collection in self.collections:
                response = self.stac_client.collections[collection]
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

    def getImages(self):
        """Return a list with available images collected by STAC."""
        return self.data_images

    def getDataCube(self):
        """Return a xarray with available data cube."""
        return self.data_array

    def getTimeSeries(self, band, start_date, end_date, lon, lat):
        _image = None
        _start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d')
        _end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d')
        for time in self.timeline:
            if time.year == _start_date.year and \
                time.month == _start_date.month:
                _image = self.data_images[time]
                break
        if not _image:
            _image = self.data_images[self.timeline[0]]
        point = _image._afimCoordsToPoint(lon, lat, band)
        return self.getDataCube().loc[
            band,
            start_date:end_date,
            point[0], point[1]
        ]

    def searchByBand(self, band):
        return self.getDataCube().loc[band]

    def convertDataFrame(self, time_slice):
        return self.getDataCube().isel(time = slice(slice)).to_dataframe()

    def calculateNDVI(self, time):
        _date = self.getDataCube().sel(time = time, method="nearest").time.values
        _date = datetime.datetime.utcfromtimestamp(_date.tolist()/1e9)
        _data = self.data_images[_date].getNDVI()
        _timeline = [_date]
        _x = list(range(0, len(_data[0])))
        _y = list(range(0, len(_data)))
        result = xr.DataArray(
            np.array([_data]),
            coords=[_timeline, _y, _x],
            dims=["time", "y", "x"],
            name=["ImageNDVI"]
        )
        result.attrs = self.getDescription()
        return result

    def calculateNDWI(self, time):
        _date = self.getDataCube().sel(time = time, method="nearest").time.values
        _date = datetime.datetime.utcfromtimestamp(_date.tolist()/1e9)
        _data = self.data_images[_date].getNDWI()
        _timeline = [_date]
        _x = list(range(0, len(_data[0])))
        _y = list(range(0, len(_data)))
        result = xr.DataArray(
            np.array([_data]),
            coords=[_timeline, _y, _x],
            dims=["time", "y", "x"],
            name=["ImageNDWI"]
        )
        result.attrs = self.getDescription()
        return result

    def calculateNDBI(self, time):
        _date = self.getDataCube().sel(time = time, method="nearest").time.values
        _date = datetime.datetime.utcfromtimestamp(_date.tolist()/1e9)
        _data = self.data_images[_date].getNDBI()
        _timeline = [_date]
        _x = list(range(0, len(_data[0])))
        _y = list(range(0, len(_data)))
        result = xr.DataArray(
            np.array([_data]),
            coords=[_timeline, _y, _x],
            dims=["time", "y", "x"],
            name=["ImageNDBI"]
        )
        result.attrs = self.getDescription()
        return result

    def calculateColorComposition(self, time):
        _date = self.getDataCube().sel(time = time, method="nearest").time.values
        _date = datetime.datetime.utcfromtimestamp(_date.tolist()/1e9)
        _data = self.data_images[_date].getRGB()
        _timeline = [_date]
        _x = list(range(0, len(_data[0])))
        _y = list(range(0, len(_data)))
        _rgb = ["red", "green", "blue"]
        result = xr.DataArray(
            np.array([_data]),
            coords=[_timeline, _y, _x, _rgb],
            dims=["time", "y", "x", "rgb"],
            name=["ColorComposition"]
        )
        result.attrs = self.getDescription()
        return result
