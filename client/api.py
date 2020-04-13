import requests
import json
import sys

sys.path.append(sys.path[0].replace("client", ""))
from config import server_address, server_port


class API:
    def __init__(self):
        self._data = {}
        res = requests.get('http://' + server_address + ':' + str(server_port))
        self._data = dict(json.loads(res.text))

    # Get JSON from Flask API
    def get_data(self):
        return self._data

    # What the server wants the client do. work? sleep?
    def get_state(self):
        return self._data["state"]
