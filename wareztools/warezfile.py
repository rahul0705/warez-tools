"""
author: Rahul Mohandas
"""
import os
import logging

module_logger = logging.getLogger(__name__)

class WarezFile(object):


    def __init__(self, warezfile):
        self.__path = os.path.dirname(warezfile)
        self.__filename = os.path.splitext(os.path.basename(warezfile))[0]
        self.__extension = os.path.splitext(warezfile)[1]

    @property
    def path(self):
        return self.__path
    @path.setter
    def path(self, path):
        """Change the path of the file

        This function will move the file's path.

        Args:
            path (str): the new path of the file.
        """
        prev_self_file = self.file
        self.__path = path
        if prev_self_file != self.file:
            module_logger.debug('renaming path; moving file %s to %s',
                                prev_self_file,
                                self.file)
            os.rename(prev_self_file, self.file)

    @property
    def filename(self):
        return self.__filename
    @filename.setter
    def filename(self, filename):
        """Change the filename of the file

        This function will rename the file.

        Args:
            filename (str): the new name of the file.
        """
        prev_self_file = self.file
        self.__filename = filename
        if prev_self_file != self.file:
            module_logger.debug('renaming filename; moving file %s to %s',
                                prev_self_file,
                                self.file)
            os.rename(prev_self_file, self.file)

    @property
    def extension(self):
        return self.__extension

    @property
    def file(self):
        """Get the full file name

        This function will return the file including the path self.

        Returns:
            String of the file name with the path.
        """
        return os.path.join(self.path,
                            '{0}{1}'.format(self.filename,
                                            self.extension))
    @property
    def scene_group(self):
        """Get the scene group

        This function will find the scene group that release this file using
        the filename. This is done by taking the contents after the hypen in
        the filename.

        Returns:
            String of the scene group.

        """
        # always return tuple of size 3 even if not found
        return self.filename.partition('-')[2]
