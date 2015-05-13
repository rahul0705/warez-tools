"""
author: Rahul Mohandas
"""
import re
import os

class WarezFile(object):
    """Warez File Object
    """

    def __init__(self, filename):
        self.__file = filename
        self.filename = os.path.basename(filename)
        self.path = os.path.dirname(filename)

    def remove_group(self):
        """Remove the scene group from the name of the file
        """
        self.filename = re.sub(r"\-.*?(\.\w{3})\Z", r"\1", self.filename)

    def remove_proper(self):
        """Remove the proper tag from the name of the file
        """
        self.filename = re.sub(r"proper\.",
                               r"",
                               self.filename,
                               flags=re.IGNORECASE)

    def remove_repack(self):
        """Remove the repack tag from the name of the file
        """
        self.filename = re.sub(r"repack\.",
                               r"",
                               self.filename,
                               flags=re.IGNORECASE)

    def remove_internal(self):
        """Remove the internal tag from the name of the file
        """
        self.filename = re.sub(r"internal\.",
                               r"",
                               self.filename,
                               flags=re.IGNORECASE)

    def move_to_movie(self):
        """Move a file into the movie directory
        """
        self.path = os.path.join(self.path, "movie")

    def move_to_tv(self):
        """Move a file into the tv directory
        """
        self.path = os.path.join(self.path, "tv")

    def fix_show(self):
        """Fix the show format so it match .*.sSSeEE[eEE]..*
        """
        #Handle .SEE. or .SEEEE. to .sSeEE. or .sSeEEEE.
        self.filename = re.sub(r"\.(\d)((\d{2}){1,2})\.",
                               r".s\g<1>e\g<2>.",
                               self.filename)

        #Handle .sS?eEE. or .sS?eEE?EE. to .s0SeEE. or .s0SeEEEE.
        self.filename = re.sub(r"\.([S|s])(\d)\.?([E|e]\d{2})\.?((\d{2})?)\.",
                               r".\g<1>0\g<2>\g<3>\g<4>.",
                               self.filename)

        #Handle eEEEE. to eEEeEE.
        self.filename = re.sub(r"(([E|e])\d{2})\.?(\d{2})\.",
                               r"\g<1>\g<2>\g<3>.",
                               self.filename)

        #Handle .sSS.eEE. to .sSSeEE.
        self.filename = re.sub(r"\.([S|s]\d+)\.([E|e]\d+)\.",
                               r".\g<1>\g<2>.",
                               self.filename)

        #Handle eEE.eEE to eEEeEE
        self.filename = re.sub(r"([E|e]\d+)\.?([E|e]\d+)",
                               r"\g<1>\g<2>",
                               self.filename)
