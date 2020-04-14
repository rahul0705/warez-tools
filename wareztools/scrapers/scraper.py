"""
author: Rahul Mohandas
"""

class Scraper(object):

    def __init__(self):
        pass

    def get_show_id(self, name):
        raise NotImplementedError()

    def validate_show(self, name):
        raise NotImplementedError()

    def validate_show_season(self, name, season):
        raise NotImplementedError()

    def validate_show_episode(self, name, season, episode):
        raise NotImplementedError()

    def get_movie_id(self, name):
        raise NotImplementedError()

    def validate_movie(self, name):
        raise NotImplementedError()
