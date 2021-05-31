#!/usr/bin/env python

import configparser

from flask.globals import request

from src.DatabaseManager import DatabaseManager, supported_get_params
from src.Serializer import Serializer

from flask import Flask, jsonify

debug = False
app = Flask(__name__)

config = configparser.ConfigParser()
config.read("config.ini")


@app.route('/', methods=["GET"])
def get_json():
    # no parameters provided
    if (not bool(request.args) or not config['Endpoint'].getboolean('AllowParams')):
        output = ""
        with open(config['Common']['TargetJson'], 'r') as f:
            output = f.read()
        return app.response_class(
            response=output,
            status=200,
            mimetype='application/json'
        )

    # some parameters provided: must validate first
    params = {}
    for key in request.args.keys():
        if (not key in supported_get_params.keys()):
            return jsonify(get_key_error()), 400
        if (not supported_get_params[key]["validator"](request.args.get(key))):
            return jsonify(get_value_error(key)), 400

        params[key] = request.args.get(key)

    polls = []
    last_update = ""
    with DatabaseManager(config['Common']['DatabaseFile']) as db_manager:
        polls = db_manager.get_polls(params)
        last_update = db_manager.get_last_update()

    metadata = {
        "last_update": last_update
    }

    serializer = Serializer()
    result_json = serializer.get_json(polls, metadata)

    return app.response_class(
        response=result_json,
        status=200,
        mimetype='application/json'
    )


def get_key_error():
    return {
        "error": "Unsupported parameter",
        "message": "This parameter is not supported. See the docs for supported parameters."
    }


def get_value_error(key):
    return {
        "error": "Unsupported parameter value",
        "message": "Incorrect value for parameter '" + key + "': " + supported_get_params[key]["help"]
    }
