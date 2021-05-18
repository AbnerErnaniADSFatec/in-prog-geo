"""
4. API - EO Data Cube.
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

app = Flask(__name__)
app.json_encoder = CustomJSONEncoder
CORS(app)

@app.route("/eocube/collections", methods=['GET'])
def collections():
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
    """
    dados de testes:
    {
        "collections": ["CB4_64_16D_STK-1"],
        "bbox": [-46.01348876953125, -23.08478515994374, -45.703125, -23.34856015148709],
        "interval": ["2018-08-01","2019-07-31"],
        "limit": 10
    }
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
