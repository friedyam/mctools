import json
import requests


class SickRage(object):

    def __init__(self, base_url, port, api_key, default_pp_path):
        self.base_url = base_url
        self.port = port
        self.api_key = api_key
        self.default_pp_path = default_pp_path

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

    def list_shows(self, sort="name", detailed=False):
        cmd = "shows"
        params = {
            'cmd': cmd,
            'sort': sort
        }

        shows = self.get(params)['data']

        return shows

    def show(self, indexerid):
        pass

    def post_process(self, path=None, return_data=1):
        cmd="postprocess"
        if not path:
            path = self.default_pp_path
        params = {
            'cmd': cmd,
            'path': path,
            'return_data': return_data
        }

        postprocess = self.get(params)

        return postprocess


