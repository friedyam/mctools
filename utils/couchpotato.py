import json
import requests


class CouchPotato(object):

    def __init__(self, url, port, api_key):
        self.url = url
        self.port = port
        self.api_key = api_key

    def url(self):
        return "http://{0}:{1}/api/{2}".format(self.base_url, self.port, self.api_key)

    def get(self, params, data=None):
        try:
            r = requests.post(self.url(), params=params, data=data)
            return r.json()
        except json.JSONDecodeError:
            print("There was an error decoding the response json")

    def post(self, params, data=None):
        try:
            r = requests.post(self.url(), params=params, data=data)
            return r.json()
        except json.JSONDecodeError:
            print("There was an error decoding the response json")
