"""
author: Rahul Mohandas
"""
import re
import os

from  wareztools.warezfile import WarezFile
import wareztools.scrapers.themoviedb

class Video(WarezFile):
    """Warez File Object
    """

    def __init__(self, warezfile):
        super(Video, self).__init__(warezfile)
        self.db = wareztools.scrapers.themoviedb.TheMovieDB()

    def move_to_movie(self):
        """Move a file into the movie directory
        """
        if "movie" not in self.path:
            new_path = os.path.join(self.path, "movie")
            if not os.path.exists(new_path):
                os.makedirs(new_path)
            self.path = new_path

    def move_to_tv(self):
        """Move a file into the tv directory
        """
        if "tv" not in self.path:
            new_path = os.path.join(self.path, "tv")
            if not os.path.exists(new_path):
                os.makedirs(new_path)
            self.path = new_path

    def remove_group(self):
        """Remove the scene group from the name of the file
        """
        self.filename = self.filename.partition("-")[0]

    def remove_proper(self):
        """Remove the proper tag from the name of the file
        """
        self.filename = re.sub(r"\.proper",
                               r"",
                               self.filename,
                               flags=re.IGNORECASE)

    def remove_repack(self):
        """Remove the repack tag from the name of the file
        """
        self.filename = re.sub(r"\.repack",
                               r"",
                               self.filename,
                               flags=re.IGNORECASE)

    def remove_internal(self):
        """Remove the internal tag from the name of the file
        """
        self.filename = re.sub(r"\.internal",
                               r"",
                               self.filename,
                               flags=re.IGNORECASE)

    def get_show_info(self):
        name = None
        season = None
        episodes = list()
        original_filename = self.filename
        self.__fix_season_episode_format()
        m = self.__get_show_regex()
        if m:
            name = m.group(1)
            season = m.group(2).lower().lstrip("s")
            for episode in m.group(4).lower().lstrip("e").split("e"):
                episode = episode.lstrip("e")
                if not self.db.validate_show_episode(name, season, episode):
                    self.filename = original_filename
                    return (None, None, list())
                episodes.append(episode)
        return (name, season, episodes)

    def __get_show_regex(self):
        return re.match(r"(.*)\.(s(\d{2}))((e\d{2})+)",
                        self.filename,
                        flags=re.IGNORECASE)

    def __season_episode_regex(self):
        return re.match(r"(.*)\.(s(\d{1,2}))\.?((e\d{2}\.?)+)",
                        self.filename,
                        flags=re.IGNORECASE)

    def __fix_season_episode_format(self):
        """Fix the show format so it match .*.sSSeEE[eEE]..*
        """
        if self.__get_show_regex():
            return

        if not self.__season_episode_regex():
            #Handle .SEE. or .SEEEE. to .sSeEE. or .sSeEEEE.
            self.filename = re.sub(r"\.(\d{1,2})((\d{2}){1,2})\.",
                                  r".s\g<1>e\g<2>.",
                                  self.filename,
                                  flags=re.IGNORECASE)

        #Handle .sS?eEE. or .sS?eEE?EE. to .s0SeEE. or .s0SeEEEE.
        self.filename = re.sub(r"\.(s)(\d)\.?(e\d{2})\.?((\d{2})?)\.",
                              r".\g<1>0\g<2>\g<3>\g<4>.",
                              self.filename,
                              flags=re.IGNORECASE)

        #Handle eEEEE. to eEEeEE.
        self.filename = re.sub(r"(e\d{2})\.?(\d{2})\.",
                              r"\g<1>e\g<2>.",
                              self.filename,
                              flags=re.IGNORECASE)

        #Handle .sSS.eEE. to .sSSeEE.
        self.filename = re.sub(r"\.(s\d+)\.(e\d+)\.",
                              r".\g<1>\g<2>.",
                              self.filename,
                              flags=re.IGNORECASE)

        #Handle eEE.eEE to eEEeEE
        self.filename = re.sub(r"(e\d+)\.?(?=(e\d+))",
                              r"\g<1>",
                              self.filename,
                              flags=re.IGNORECASE)
