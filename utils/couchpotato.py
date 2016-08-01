from collections import namedtuple
import json
import requests

movie_fields = [
    'title',
    'released',
    'plot',
    'runtime',
    'genres',
    'directors',
    'writers',
    'rating',
    'status',
    'id',
    'location',
    'quality'
]
Movie = namedtuple("Movie", field_names=movie_fields)


class CouchPotato(object):

    def __init__(self, base_url, port, api_key):
        self.base_url = base_url
        self.port = port
        self.api_key = api_key

    def url(self, cmd):
        return "http://{0}:{1}/api/{2}/{3}".format(self.base_url, self.port, self.api_key, cmd)

    def get(self, cmd, params=None, data=None):
        try:
            r = requests.get(self.url(cmd=cmd), params=params, data=data)
            return r.json()
        except json.JSONDecodeError:
            print("There was an error decoding the response json")

    def post(self, cmd, params=None, data=None):
        try:
            r = requests.post(self.url(cmd=cmd), params=params, data=data)
            return r.text
        except json.JSONDecodeError:
            print("There was an error decoding the response json")

    def restart(self):
        cmd = 'app.restart'
        msg = self.post(cmd)

        return msg

    def renamer(self):
        cmd = 'renamer.scan'
        msg = self.post(cmd)
        
        return msg

    def search(self, query):
        cmd = 'search'
        params = {
            'q': query
        }

        results = self.get(cmd, params=params)['movies']

        movies = []
        for movie in results:
            try:
                movies.append(
                    Movie(
                        title=movie.get('original_title', ''),
                        released=movie.get('year', 0),
                        plot=movie.get('plot', ''),
                        runtime=movie.get('runtime', 0),
                        genres=movie.get('genre', []),
                        directors=movie.get('directors', []),
                        writers=movie.get('writers', []),
                        rating=movie.get('rating', {}).get('imdb', [None])[0],
                        status="In Library" if movie.get('in_library', False) else "Missing",
                        id=movie.get('imdb', ''),
                        location=None,
                        quality=None
                    )
                )
            except KeyError:
                print(json.dumps(movie, indent=4))
                raise

        return movies

    def add_movie(self):
        cmd = 'movie.add'

    def list_movies(self, search=None):
        cmd = 'movie.list'
        params = {
            'status': ['done']
        }

        if search:
            params['search'] = search

        results = self.get(cmd, params=params)['movies']

        movies = []
        for movie in results:
            release_info = [r for r in movie['releases'] if 'files' in r]
            try:
                movies.append(
                    Movie(
                        title=movie['title'],
                        released=movie['info']['released'] if 'released' in movie['info'] else movie['info']['year'],
                        plot=movie['info']['plot'],
                        runtime=movie['info']['runtime'],
                        genres=movie['info']['genres'],
                        directors=movie['info']['directors'],
                        writers=movie['info']['writers'],
                        rating=movie['info']['rating']['imdb'][0],
                        status=movie['status'],
                        id=movie['_id'],
                        location=release_info[0]['files']['movie'][0],
                        quality=release_info[0]['quality']
                    )
                )
            except KeyError:
                print(json.dumps(movie, indent=4))
                raise

        return movies

    def search_torrents(self):
        cmd = 'movie.searcher.full_search'
