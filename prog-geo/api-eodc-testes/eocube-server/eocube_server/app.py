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

import random

import stac
from _datetime import date
from eocube_server import config
from flask import Flask, abort, request
from flask.json import JSONEncoder
from flask_cors import CORS, cross_origin
from flask_jsonpify import *


class CustomJSONEncoder(JSONEncoder):
    """Custom JSON Encoder for validate the API response."""
    def default(self, obj):
        try:
            if isinstance(obj, date):
                return obj.isoformat()
            iterable = iter(obj)
        except TypeError:
            pass
        else:
            return list(iterable)
        return JSONEncoder.default(self, obj)

# Criando o app com a biblioteca Flask
# com este app é possível definir as rotas e as
# regras de CROSS ORIGIN
app = Flask(__name__)
app.json_encoder = CustomJSONEncoder
CORS(app)

# App.route define as rotas e os métodos permitidos
@app.route("/eocube/collections", methods=['GET'])
def collections():
    """Get a list with available collections from STAC.

    ## Parameters

    ### token : string, optional

        The BDC user token.

    ## Raise

    ### HTTPError

        If the STAC server is out of service.
    """
    token = request.args.get('token')
    try:
        service = stac.STAC(
            config.STAC_URL,
            access_token=token
        )
        return jsonify({
            'collections': list(service.collections.keys())
        })
    except:
        return jsonify({
            'code': '403',
            'message': 'Access error, forbidden!'
        })

@app.route("/eocube/describe/<collection_name>", methods=['GET'])
def describe(collection_name):
    """Get a description with available collection name from STAC.

    ## Parameters

    ### collection_name : string, required

        The collection name from list collections.

    ### token : string, required

        The BDC user token.

    ## Raise

    ### HTTPError

        If the STAC server is out of service.
    """
    token = request.args.get('token')
    try:
        service = stac.STAC(
            config.STAC_URL,
            access_token=token
        )
        return jsonify(service.collections[collection_name])
    except:
        return jsonify({
            'code': '403',
            'message': 'Access error, forbidden!'
        })

@app.route("/eocube/search", methods=['POST'])
def search():
    """Get a description with available collection name from STAC.

    ## Parameters

    ### token : string, required

        The BDC user token.

    ## JSON Object

    ### Test data for POST:

        {
            "collections": ["CB4_64_16D_STK-1"],
            "bbox": [-46.01348876953125, -23.08478515994374, -45.703125, -23.34856015148709],
            "interval": ["2018-08-01","2019-07-31"],
            "limit": 10
        }

    ## Raise

    ### HTTPError

        If the STAC server is out of service.
    """
    token = request.args.get('token')
    if request.method == 'POST':
        try:
            collections = request.json['collections']
            bbox = tuple(request.json['bbox'])
            start_date = request.json['interval'][0]
            end_date = request.json['interval'][1]
            limit = request.json['limit']
            try:
                query = {
                    'collections': collections,
                    'bbox': bbox,
                    'datetime': f'{start_date}/{end_date}',
                    'limit': limit
                }
                items = stac.STAC(
                    config.STAC_URL,
                    access_token=token
                ).search(query)
                return jsonify({
                    "query" : query,
                    "result": items.features
                })
            except:
                return jsonify({
                    'code': '403',
                    'message': 'Access error, forbidden!'
                })
        except:
            return jsonify({
                'code': '400',
                'message': 'Request JSON error!'
            })
