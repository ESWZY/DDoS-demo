import requests
import json

from config import server_address, server_port


class API:
    def __init__(self):
        self._data = {}

    # Get JSON from Flask API
    def get_data(self):
        req = requests.get('http://' + server_address + ':' + str(server_port))
        self._data = dict(json.loads(req.text))
        return self._data


