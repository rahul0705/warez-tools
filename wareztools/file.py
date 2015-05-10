"""
author: Rahul Mohandas
"""
import re
import os

class WarezFile():
    """Warez File Object
    """

    def __init__(self, filename):
        self.__file = filename
        self.filename = os.path.basename(filename)

    def remove_group(self):
        self.filename = re.sub(r"\-.*?(\.\w{3})\Z", r"\1", self.filename)

    def fix_show(self):
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
