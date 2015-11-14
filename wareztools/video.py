"""
author: Rahul Mohandas
"""
import re
import os

import scrapers.themoviedb

class Video(object):
    """Warez File Object
    """
    api_key = "fc2ba5302e694c0676d0f8667832ac83"

    def __init__(self, video):
        self.__video = video
        self.path = os.path.dirname(video)
        self.__filename = os.path.basename(os.path.splitext(video)[0])
        self.extension = os.path.splitext(video)[1]
        self.db = scrapers.themoviedb.TheMovieDB(Video.api_key)

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

    def rename_show(self):
        name, season, episodes = self.get_show_info()
        if not name:
            return
        self.remove_group()
        return os.path.join(self.path, "{0}{1}".format(self.__filename,
                                                       self.extension))

    def __get_show_regex(self):
        return re.match(r"(.*)\.(s(\d{2}))((e\d{2})+)",
                        self.__filename,
                        flags=re.IGNORECASE)

    def __fix_season_episode_format(self):
        """Fix the show format so it match .*.sSSeEE[eEE]..*
        """
        if self.__get_show_regex():
            return

        #Handle .SEE. or .SEEEE. to .sSeEE. or .sSeEEEE.
        self.__filename = re.sub(r"\.(\d)((\d{2}){1,2})\.",
                              r".s\g<1>e\g<2>.",
                              self.__filename,
                              flags=re.IGNORECASE)

        #Handle .sS?eEE. or .sS?eEE?EE. to .s0SeEE. or .s0SeEEEE.
        self.__filename = re.sub(r"\.(s)(\d)\.?(e\d{2})\.?((\d{2})?)\.",
                              r".\g<1>0\g<2>\g<3>\g<4>.",
                              self.__filename,
                              flags=re.IGNORECASE)

        #Handle eEEEE. to eEEeEE.
        self.__filename = re.sub(r"(e\d{2})\.?(\d{2})\.",
                              r"\g<1>e\g<2>.",
                              self.__filename,
                              flags=re.IGNORECASE)

        #Handle .sSS.eEE. to .sSSeEE.
        self.__filename = re.sub(r"\.(s\d+)\.(e\d+)\.",
                              r".\g<1>\g<2>.",
                              self.__filename,
                              flags=re.IGNORECASE)

        #Handle eEE.eEE to eEEeEE
        self.__filename = re.sub(r"(e\d+)\.?(?=(e\d+))",
                              r"\g<1>",
                              self.__filename,
                              flags=re.IGNORECASE)

if __name__ == "__main__":
    import sys
    wf = Video(sys.argv[1])
    print wf.get_show_info()
    print wf.rename_show()
