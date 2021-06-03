#!/usr/bin/env python

import configparser
import logging
import json
import os
import tempfile
import traceback
import zipfile

from datetime import datetime
from jsonschema import validate, ValidationError
from typing import List

from src.DatabaseManager import DatabaseManager
from src.ProtocolParser import ProtocolParser
from src.Serializer import Serializer


def load_config() -> configparser.ConfigParser:
    config = configparser.ConfigParser()
    config.read("config.ini")

    return config


def setup_logging(logfile, debug=False):
    logging.basicConfig(format='[%(asctime)s] %(levelname)s: %(message)s', filename=logfile,
                        level=logging.DEBUG if debug else logging.INFO)


def load_processed_files(db_manager: DatabaseManager) -> List[str]:
    return db_manager.get_processed_filenames()


def load_stored_files(protocols_dir: str) -> List[str]:
    return os.listdir(protocols_dir)


def get_new_files(db_manager: DatabaseManager, protocols_dir: str) -> List[str]:
    p_files = load_processed_files(db_manager)
    s_files = load_stored_files(protocols_dir)

    output = []
    for s_file in s_files:
        if (not s_file in p_files and s_file.endswith(".zip")):
            output.append(s_file)

    return output


def unzip_file(source: str, target: str):
    with zipfile.ZipFile(source, 'r') as zip_ref:
        zip_ref.extractall(target)


def create_static_json(db_manager: DatabaseManager) -> str:
    all_polls = db_manager.get_polls({})

    metadata = {
        "last_update": db_manager.get_last_update()
    }

    serializer = Serializer()
    result_json = serializer.get_json(all_polls, metadata)

    return result_json


def is_json_valid(json_data: str) -> bool:
    json_dict = json.loads(json_data)
    json_schema = {}
    with open("output-schema.json", 'r') as f:
        json_schema = json.load(f)

    try:
        validate(json_dict, json_schema)
        return True
    except ValidationError:
        return False


if __name__ == '__main__':
    config = load_config()

    debug = config['Parser'].getboolean('Debug')
    setup_logging(config['Parser']['LogFile'], debug)

    logging.info("starting daemon.py")
    logging.debug("debug mode on")

    db_man = DatabaseManager(config['Common']['DatabaseFile'])
    logging.debug("loaded db '" + config['Common']['DatabaseFile'] + "'")

    new_files = get_new_files(db_man, config['Parser']['ProtocolsDir'])
    logging.debug("found " + str(len(new_files)) + " new files in directory '" +
                  config['Parser']['ProtocolsDir'] + "'")

    parser = ProtocolParser()

    total_zips = 0
    total_html = 0

    for new_file in new_files:
        logging.debug("processing file '" + new_file + "'")

        with tempfile.TemporaryDirectory() as target_dir:
            try:
                unzip_file(os.path.join(
                    config['Parser']['ProtocolsDir'], new_file), target_dir)
            except Exception:
                logging.warning("file '" + new_file + "' is not a valid .zip!")
                continue

            protocols = os.listdir(target_dir)

            for protocol in protocols:
                if (not protocol.endswith(".html")):
                    logging.debug("'" + protocol +
                                  "' is not .html -> skipping")
                    continue
                try:
                    logging.debug("parsing '" + protocol + "' in '" + new_file + "'")
                    poll = parser.parse_file(
                        os.path.join(target_dir, protocol))
                except Exception as e:
                    logging.warning("couldn't parse protocol: file '" + protocol + "' in '" +
                                    new_file + "' is not a valid .html protocol!")
                    logging.debug(str(e) + "\n" + traceback.format_exc())
                    continue
                db_man.save_poll(poll)

                total_html += 1

            db_man.save_processed_file(
                new_file, datetime.now().strftime("%Y-%m-%dT%H:%M:%S+00:00"))

            total_zips += 1

    if (len(new_files) > 0):
        result_json = create_static_json(db_man)
        logging.debug("saving new JSON to '" +
                      config['Common']['TargetJson'] + "'")

        with open(config['Common']['TargetJson'], 'w') as outfile:
            outfile.write(result_json)

        if (not is_json_valid(result_json)):
            logging.warning("newly created JSON '" +
                            config['Common']['TargetJson'] + "' is not valid (schema differs)!")
        else:
            logging.debug("JSON validated successufully")

    db_man.close()

    if (total_zips > 0):
        logging.info("stopping daemon.py: successfully processed " +
                     str(total_zips) + " zip files and " + str(total_html) + " protocols")
    else:
        logging.info("stopping daemon.py: no new zip files")
