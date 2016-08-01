from collections import namedtuple
import json
import requests


class Kodi(object):
    def __init__(self, base_url, port, api_key):
        self.base_url = base_url
        self.port = port

    def url(self):
        return "http://{0}:{1}/jsonrpc".format(self.base_url, self.port)

    def build_request(self, cmd, params):
        request = {
            'request': {
                'jsonrpc': '2.0',
                'id': 1,
                'method': cmd,
                'params': params
            }
        }

        return request

    def get(self, cmd, params=None, data=None):
        try:
            r = requests.get(self.url(), params=self.build_request(cmd, params), data=data)
            return r.json()
        except json.JSONDecodeError:
            print("There was an error decoding the response json")

    def post(self, cmd, params=None, data=None):
        try:
            r = requests.post(self.url(), params=self.build_request(cmd, params), data=data)
            return r.text
        except json.JSONDecodeError:
            print("There was an error decoding the response json")

