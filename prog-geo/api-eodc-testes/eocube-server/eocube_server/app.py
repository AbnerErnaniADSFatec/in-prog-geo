"""
4. API - EO Data Cube.
"""

import random

import stac
from eocube_server import config

from flask import Flask, request, abort
from flask_cors import CORS, cross_origin
from flask_jsonpify import *
from flask.json import JSONEncoder
from _datetime import date

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

@app.route("/<number>", methods=['GET'])
def hello(number):
    aux = []
    if not number:
        number = 10
    for i in range(int(number)):
        aux.append(
            random.randint(0,int(number))
        )
    return jsonify({
        'text':'Hello World!!!',
        'random_numbers':aux
    })

@app.route("/collections", methods=['GET'])
def get_collections():
    config.ACCESS_TOKEN = request.args.get('token')
    try:
        service = stac.STAC(
            config.STAC_URL,
            access_token=config.ACCESS_TOKEN
        )
        return jsonify({
            'collections': list(service.collections.keys())
        })
    except:
        return jsonify({
            'code': '403',
            'message': 'Access error, forbidden!'
        })

