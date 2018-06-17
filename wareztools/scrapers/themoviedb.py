"""
author: Rahul Mohandas
"""
import json
try:
    from urllib import urlencode
    from urllib2 import urlopen
    from urllib2 import Request
    from urllib2 import HTTPError
except ImportError:
    from urllib.parse import urlencode
    from urllib.request import urlopen
    from urllib.request import Request
    from urllib.error import HTTPError

import wareztools.scrapers.scraper

class TheMovieDB(wareztools.scrapers.scraper.Scraper):
    api_key = "fc2ba5302e694c0676d0f8667832ac83"

    def __init__(self, api_key=None):
        if not api_key:
            api_key = TheMovieDB.api_key
        super(TheMovieDB, self).__init__(api_key=api_key)
        self.base_url = "https://api.themoviedb.org/3"
        self.__reset_request()

    def __reset_request(self):
        self.request_args = dict([("api_key", self.api_key)])
        self.request_headers = dict([("Accept", "application/json")])

    def __fix_name(self, name):
        name = name.replace(".", " ")
        return name

    def get_show_id(self, name):
        self.__reset_request()
        name = self.__fix_name(name)
        self.request_args["query"] = name
        url = "{0}/search/tv".format(self.base_url)
        url = "{0}?{1}".format(url, urlencode(self.request_args))
        request = Request(url, headers=self.request_headers)
        try:
            response_body = json.loads(urlopen(request).read())
        except HTTPError:
            raise
        if not response_body["total_results"]:
            raise KeyError("Nothing found")
        if response_body["total_results"] > 1:
            raise ValueError("Too may results")
        return response_body["results"][0]["id"]

    def validate_show(self, name):
        try:
            if self.get_show_id(name):
                return True
            return False
        except KeyError:
            return False

    def validate_show_season(self, name, season):
        self.__reset_request()
        url = "{0}/tv/{1}/season/{2}".format(self.base_url,
                                             self.get_show_id(name),
                                             season)
        url = "{0}?{1}".format(url, urlencode(self.request_args))
        request = Request(url, headers=self.request_headers)
        try:
            response_body = json.loads(urlopen(request).read())
            return True
        except HTTPError:
            return False

    def validate_show_episode(self, name, season, episode):
        self.__reset_request()
        url = "{0}/tv/{1}/season/{2}/episode/{3}".format(self.base_url,
                                                         self.get_show_id(name),
                                                         season,
                                                         episode)
        url = "{0}?{1}".format(url, urlencode(self.request_args))
        request = Request(url, headers=self.request_headers)
        try:
            response_body = json.loads(urlopen(request).read())
            return True
        except HTTPError:
            return False

    def get_movie_id(self, name):
        self.__reset_request()
        name = self.__fix_name(name)
        self.request_args["query"] = name
        url = "{0}/search/movie".format(self.base_url)
        url = "{0}?{1}".format(url, urlencode(self.request_args))
        request = Request(url, headers=self.request_headers)
        try:
            response_body = json.loads(urlopen(request).read())
        except HTTPError:
            raise
        if not response_body["total_results"]:
            raise KeyError("Nothing found")
        if response_body["total_results"] > 1:
            raise ValueError("Too may results")
        return response_body["results"][0]["id"]

    def validate_movie(self, name):
        try:
            if self.get_movie_id(name):
                return True
            return False
        except KeyError:
            return False
