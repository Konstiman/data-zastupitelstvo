#!/usr/bin/python

import cgi
import cgitb
import configparser
import json

from src.DatabaseManager import DatabaseManager, supported_get_params
from src.Serializer import Serializer


def print_output(json, status="200 OK"):
    print('Content-Type: application/json')
    print('Status: ' + status)
    print('')

    print(json)
    exit(0)


debug = False
if (debug):
    cgitb.enable()

config = configparser.ConfigParser()
config.read("config.ini")

arguments = cgi.FieldStorage()

# no parameters provided
if (len(arguments.keys()) == 0):
    output = ""
    with open(config['Parser']['TargetJson'], 'r') as f:
        output = f.read()
    print_output(output)

# some parameters provided: must validate

params = {}
for key in arguments.keys():
    if (not key in supported_get_params.keys()):
        print_output(json.dumps({"error": "Unsupported parameter",
                                 "message": "This parameter is not supported. See the docs for supported parameters."}), "400 Bad Request")
    if (not supported_get_params[key]["validator"](arguments.getvalue(key))):
        print_output(json.dumps({"error": "Unsupported parameter value", "message": "Incorrect value for parameter '" +
                                 key + "': " + supported_get_params[key]["help"]}), "400 Bad Request")
    
    params[key] = arguments.getvalue(key)

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

print_output(result_json)

# src: https://techexpert.tips/apache/apache-enable-python-cgi/
