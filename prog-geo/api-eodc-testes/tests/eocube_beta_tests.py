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

from ipywidgets import interact
import matplotlib.pyplot as plt

import datetime
import json
import warnings

import numpy as np
import requests
import stac
import wtss
import xarray as xr
from dask import delayed

from eocube import config

from .image import Image
from .utils import Utils
from .spectral import Spectral

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
                    band_common_name = str(band.get('common_name', ''))
                    band_name = str(band.get('name'))
                    # Cria um dicionário com cada chave sendo o nome comum da banda e o nome dado pelo item
                    if band_common_name in self.query_bands:
                        bands[band_common_name] = band.get('name')
                    elif band_name in self.query_bands:
                        bands[band_name] = band_name
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
                data = delayed(image.getBand)(band)
                # data = image.getBand(band)
                # x = list(range(0, data.shape[1]))
                # y = list(range(0, data.shape[0]))
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

        self.description = {}
        for collection in self.collections:
            response = self.stac_client.collections[collection]
            self.description[str(response["id"])] = str(response["title"])

        self.data_array = xr.DataArray(
            np.array(time_series),
            coords=[self.query_bands, self.timeline], #, y, x],
            dims=["band", "time"], #, "y", "x"],
            name=["DataCube"]
        )
        self.data_array.attrs = self.description

    def getTimeSeries(self, band, lon, lat):
        # _image = None
        # _start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d')
        # _end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d')
        # for time in self.timeline:
        #     if time.year == _start_date.year and \
        #         time.month == _start_date.month:
        #         _image = self.data_images[time]
        #         break
        # if not _image:
        #     _image = self.data_images[self.timeline[0]]
        # point = _image._afimCoordsToPoint(lon, lat, band)
        # return self.getDataCube().loc[
        #     band,
        #     start_date:end_date,
        #     point[0], point[1]
        # ]
        _image = None
        _start_date = datetime.datetime.strptime(self.start_date, '%Y-%m-%d')
        _end_date = datetime.datetime.strptime(self.end_date, '%Y-%m-%d')
        for time in self.timeline:
            if time.year == _start_date.year and \
                time.month == _start_date.month:
                _image = self.data_images[time]
                break

        if not _image:
            _image = self.data_images[self.timeline[0]]

        point = _image._afimCoordsToPoint(lon, lat, band)

        _data = self.data_array.loc[band, self.start_date:self.end_date]

        result = []
        for raster in _data.values:
            result.append(raster.compute()[point[0]][point[1]])

        _result = xr.DataArray(
            np.array(result),
            coords=[_data.time],
            dims=["time"],
            name=[f"TimeSeries{band}"]
        )
        _result.attrs = {
            "longitude": lon,
            "latitude": lat
        }
        return _result

    def calculateNDVI(self, time):
        _date = self.data_array.sel(time = time, method="nearest").time.values
        _date = datetime.datetime.utcfromtimestamp(_date.tolist()/1e9)
        _data = self.data_images[_date].getNDVI()
        _timeline = [_date]
        _x = list(range(0, _data.shape[1]))
        _y = list(range(0, _data.shape[0]))
        result = xr.DataArray(
            np.array([_data]),
            coords=[_timeline, _y, _x],
            dims=["time", "y", "x"],
            name=["ImageNDVI"]
        )
        result.attrs = self.description
        return result

    def calculateNDWI(self, time):
        _date = self.data_array.sel(time = time, method="nearest").time.values
        _date = datetime.datetime.utcfromtimestamp(_date.tolist()/1e9)
        _data = self.data_images[_date].getNDWI()
        _timeline = [_date]
        _x = list(range(0, _data.shape[1]))
        _y = list(range(0, _data.shape[0]))
        result = xr.DataArray(
            np.array([_data]),
            coords=[_timeline, _y, _x],
            dims=["time", "y", "x"],
            name=["ImageNDWI"]
        )
        result.attrs = self.description
        return result

    def calculateNDBI(self, time):
        _date = self.data_array.sel(time = time, method="nearest").time.values
        _date = datetime.datetime.utcfromtimestamp(_date.tolist()/1e9)
        _data = self.data_images[_date].getNDBI()
        _timeline = [_date]
        _x = list(range(0, _data.shape[1]))
        _y = list(range(0, _data.shape[0]))
        result = xr.DataArray(
            np.array([_data]),
            coords=[_timeline, _y, _x],
            dims=["time", "y", "x"],
            name=["ImageNDBI"]
        )
        result.attrs = self.description
        return result

    def calculateColorComposition(self, time):
        _date = self.data_array.sel(time = time, method="nearest").time.values
        _date = datetime.datetime.utcfromtimestamp(_date.tolist()/1e9)
        _data = self.data_images[_date].getRGB()
        _timeline = [_date]
        _x = list(range(0, _data.shape[1]))
        _y = list(range(0, _data.shape[0]))
        _rgb = ["red", "green", "blue"]
        result = xr.DataArray(
            np.array([_data]),
            coords=[_timeline, _y, _x, _rgb],
            dims=["time", "y", "x", "rgb"],
            name=["ColorComposition"]
        )
        result.attrs = self.description
        return result

    def classifyDifference(self, band, start_date, end_date, limiar_min=0, limiar_max=0):
        _date = self.data_array.sel(time = start_date, method="nearest").time.values
        _date = datetime.datetime.utcfromtimestamp(_date.tolist()/1e9)
        time_1 = _date
        data_1 = self.data_images[_date].getBand(band)
        _date = self.data_array.sel(time = end_date, method="nearest").time.values
        _date = datetime.datetime.utcfromtimestamp(_date.tolist()/1e9)
        time_2 = _date
        data_2 = self.data_images[_date].getBand(band)
        spectral = Spectral()
        data_1 = spectral._format(data_1)
        data_2 = spectral._format(data_2)
        _data = None
        if spectral._validate_shape(data_1, data_2):
            diff = spectral._matrix_diff(data_1, data_2)
            _data = spectral._classify_diff(diff, limiar_min=limiar_min, limiar_max=limiar_max)
        else:
            raise ValueError("Time 1 and 2 has different shapes!")
        _timeline = [f"{time_1} - {time_2}"]
        _x = list(range(0, _data.shape[1]))
        _y = list(range(0, _data.shape[0]))
        _result = xr.DataArray(
            np.array([_data]),
            coords=[_timeline, _y, _x],
            dims=["time", "y", "x"],
            name=["ClassifyDifference"]
        )
        return _result

    def interactPlot(self, method):
        method = method.lower()
        @interact(date=self.timeline)
        def sliderplot(date):
            plt.figure(figsize=(25, 8))
            if method == 'rgb':
                plt.imshow(self.data_images[date].getRGB())
                plt.title(f'\nComposição Colorida Verdadeira {date} \n')
            elif method == 'ndvi':
                colormap = plt.get_cmap('Greens', 1000)
                plt.imshow(self.data_images[date].getNDVI(), cmap=colormap)
                plt.title(f'\nNDVI - Normalized Difference Vegetation Index {date} \n')
                plt.colorbar()
            elif method == 'ndwi':
                colormap = plt.get_cmap('Blues', 1000)
                plt.imshow(self.data_images[date].getNDWI(), cmap=colormap)
                plt.title(f'\nNDWI - Normalized Difference Water Index {date} \n')
                plt.colorbar()
            elif method == 'ndbi':
                colormap = plt.get_cmap('Greys', 1000)
                plt.imshow(self.data_images[date].getNDBI(), cmap=colormap)
                plt.title(f'\nNDBI - Normalized Difference Built-up Index {date} \n')
                plt.colorbar()
            elif method in self.query_bands:
                colormap = plt.get_cmap('Greys', 1000)
                plt.imshow(self.data_images[date].getBand(method), cmap=colormap)
                plt.title(f'\nComposição da Banda {method} {date} \n')
                plt.colorbar()
            plt.tight_layout()
            plt.show()
