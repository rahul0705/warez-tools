"""
author: Rahul Mohandas
"""
import re
import os
import itertools.izip
import itertools.islice

import wareztools.scrapers.themoviedb

class Video(object):
    """Warez File Object
    """
    api_key = "fc2ba5302e694c0676d0f8667832ac83"

    def __init__(self, video):
        self.__video = video
        self.path = os.path.dirname(video)
        self.__filename = os.path.basename(os.path.splitext(video)[0])
        self.extension = os.path.splitext(video)[1]
        self.db = None
        self._get_scraper("TheMovieDB")

    def _get_scraper(self, scraper_name):
        if scraper_name == "TheMovieDB":
            self.db = wareztools.scrapers.themoviedb.TheMovieDB(Video.api_key)
        else:
            raise ValueError("Scrapper not defined")

    @property
    def filename(self):
        return "{0}{1}".format(self.__filename, self.extension)

    def move_to_movie(self):
        """Move a file into the movie directory
        """
        if "movie" not in self.path:
            self.path = os.path.join(self.path, "movie")

    def move_to_tv(self):
        """Move a file into the tv directory
        """
        if "tv" not in self.path:
            self.path = os.path.join(self.path, "tv")

    def remove_group(self):
        """Remove the scene group from the name of the file
        """
        self.__filename = self.__filename.partition("-")[0]

    def remove_proper(self):
        """Remove the proper tag from the name of the file
        """
        self.__filename = re.sub(r"\.proper",
                               r"",
                               self.__filename,
                               flags=re.IGNORECASE)

    def remove_repack(self):
        """Remove the repack tag from the name of the file
        """
        self.__filename = re.sub(r"\.repack",
                               r"",
                               self.__filename,
                               flags=re.IGNORECASE)

    def remove_internal(self):
        """Remove the internal tag from the name of the file
        """
        self.__filename = re.sub(r"\.internal",
                               r"",
                               self.__filename,
                               flags=re.IGNORECASE)

    def get_show_info(self):
        name = None
        season = None
        episodes = list()
        original_filename = self.__filename
        self.__fix_season_episode_format()
        m = self.__get_show_regex()
        if m:
            name = m.group(1)
            season = m.group(2).lower().lstrip("s")
            for episode in m.group(4).lower().lstrip("e").split("e"):
                episode = episode.lstrip("e")
                if not self.db.validate_show_episode(name, season, episode):
                    self.__filename = original_filename
                    return (None, None, list())
                episodes.append(episode)
        return (name, season, episodes)

    def __get_show_regex(self):
        return re.match(r"(.*)\.(s(\d{2}))((e\d{2})+)",
                        self.filename,
                        flags=re.IGNORECASE)

    def __get_name_season_episode(self):
        #pad any one digit episodes
        self.__filename = re.sub(r"e(\d)(?=\D)",
                                 r"e0\g<1>",
                                 self.__filename,
                                 flags=re.IGNORECASE)
        if self.__get_show_regex():
            return
        name = None
        ending = None
        possible_match = None
        #find anything that matches [s][S]S[.][e]EE
        possible_matches = re.findall(r"s\d{1,2}(?:\.?e\d{1,2})+",
                                      self.__filename,
                                      flags=re.IGNORECASE)
        #if we match we trim the s, e, and . so that we get [S]SEE
        if possible_matches:
            possible_match = re.sub("[s|e|\.]",
                                    "",
                                    possible_matches[-1],
                                    flags=re.IGNORECASE)
        else:
            #match [S]SEE
            possible_matches = re.findall(r"\d{3,}",
                                          self.__filename,
                                          flags=re.IGNORECASE)
            if possible_matches:
                possible_match = possible_matches[-1]
        #extract season and episode from [S]SEE
        if possible_match:
            name_end = re.match(r"(.*){0}(.*)".format(possible_matches[-1]),
                                self.__filename,
                                flags=re.IGNORECASE)
            if name_end:
                name = name_end.group(1)
                ending = name_end.group(2)
            season_episode = re.search(r"(\d{1,2})((?:\d{2})+)\Z",
                                       possible_match,
                                       flags=re.IGNORECASE)
            if season_episode:
                season = "s{:02d}".format(int(season_episode.group(1)))
                episode = re.sub(r"(\d{2})",
                                 r"e\g<1>",
                                 season_episode.group(2))

                return (name, season, episode)
