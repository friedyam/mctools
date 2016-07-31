from collections import defaultdict, namedtuple
import copy
import datetime
import json
import requests
from werkzeug.datastructures import ImmutableDict

show_fields = [
    'name',
    'indexerid',
    'airs',
    'next_episode',
    'network',
    'location',
    'status',
    'genres'
]
episode_fields = [
    'show_name',
    'airdate',
    'episode_name',
    'episode_plot',
    'episode',
    'season'
]
shows_stats_fields = [
    'episodes_downloaded',
    'episodes_snatched',
    'total_episodes',
    'active_shows',
    'total_shows'
]
Show = namedtuple("Show", field_names=show_fields)
Episode = namedtuple("Episode", field_names=episode_fields)
ShowsStats = namedtuple("SnowsStats", field_names=shows_stats_fields)


class SickRage(object):

    def __init__(self, base_url, port, api_key, default_pp_path="/media/underground/Media Disk 3/TV Torrents"):
        self.base_url = base_url
        self.port = port
        self.api_key = api_key
        self.default_pp_path = default_pp_path
        self.show_ids = self.get_ids()

    def url(self):
        return "http://{0}:{1}/api/{2}".format(self.base_url, self.port, self.api_key)

    def get(self, params, data=None):
        try:
            r = requests.get(self.url(), params=params, data=data)
            return r.json()
        except json.JSONDecodeError:
            print("There was an error decoding the response json")

    def post(self, params, data=None):
        try:
            r = requests.post(self.url(), params=params, data=data)
            return r.json()
        except json.JSONDecodeError:
            print("There was an error decoding the response json")

    def get_ids(self):
        cmd = "shows"
        params = {
            'cmd': cmd,
            'sort': 'name'
        }

        data = self.get(params)['data']
        show_ids = ImmutableDict({show: data[show]['indexerid'] for show in data})

        return show_ids

    def list_shows(self):
        return [show for show in self.show_ids]

    def show(self, name):
        cmd = "show"
        params = {
            'cmd': cmd,
            'indexerid': self.show_ids[name]
        }

        data = self.get(params)['data']

        return Show(
            name=data['show_name'],
            indexerid=data['indexerid'],
            airs=data['airs'],
            next_episode=data['next_ep_airdate'],
            network=data['network'],
            location=data['location'],
            status=data['status'],
            genres=data['genre']
        )

    def future(self, sort='date', type=('soon', 'today')):
        date_format = "%Y-%m-%d %I:%M %p"
        cmd = "future"
        params = {
            'cmd': cmd,
            'sort': sort,
            'type': '|'.join(list(type))
        }

        data = self.get(params)['data']
        future = defaultdict(list)
        for t in type:
            for e in data[t]:
                date_split = e['airs'].split()
                day = date_split[0]
                future[day].append(
                    Episode(
                        show_name=e['show_name'],
                        airdate=datetime.datetime.strptime(e['airdate'] + ' ' + ' '.join(date_split[1:]), date_format),
                        episode_name=e['ep_name'],
                        episode_plot=e['ep_plot'],
                        episode=int(e['episode']),
                        season=int(e['season'])
                    )
                )

        return future

    def post_process(self, path=None, return_data=0):
        cmd = "postprocess"
        if not path:
            path = self.default_pp_path
        params = {
            'cmd': cmd,
            'path': path,
            'return_data': return_data
        }

        result = self.get(params)['result']

        return result

    def shows_stats(self):
        cmd = "shows.stats"
        params = {
            'cmd': cmd
        }

        data = self.get(params)['data']

        return ShowsStats(
            episodes_downloaded=int(data['ep_downloaded']),
            episodes_snatched=int(data['ep_snatched']),
            total_episodes=int(data['ep_total']),
            active_shows=int(data['shows_active']),
            total_shows=int(data['shows_total'])
        )

    def restart(self):
        cmd = "sb.restart"
        params = {
            'cmd': cmd
        }

        result = self.get(params)['result']

        return result


