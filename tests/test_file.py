"""
author: Rahul Mohandas
"""
import unittest
import os
import errno
import shutil
import tempfile
from wareztools.file import WarezFile

class TestWarezFile(unittest.TestCase):
    """Test the WarezFile class
    """

    def setUp(self):
        try:
            self.temp_dir = tempfile.mkdtemp()
        finally:
            try:
                shutil.rmtree(self.temp_dir)
            except OSError as exc:
                if exc.errno != errno.ENOENT:
                    raise

    def tearDown(self):
        try:
            shutil.rmtree(self.temp_dir)
        except OSError as exc:
            if exc.errno != errno.ENOENT:
                raise

    def test_remove_group_no_change(self):
        """Test to check that a groupless file does not get changed
        """
        #Test to make sure if there is no group the filename does not change
        test_filename_without_group = "test.file.name.with.no.group.txt"
        warezfile = WarezFile(os.path.join(self.temp_dir,
                                           test_filename_without_group))
        warezfile.remove_group()
        self.assertEqual(os.path.basename(warezfile.filename),
                         test_filename_without_group,
                         msg="Filename changed")

    def test_remove_group_with_group(self):
        """Test conversion of -XXXXXXX.ext to .ext
        """
        #Test to make sure if there is a group it will remove it
        test_filename_with_group = "test.file.name.with.group-GROUPNAME.txt"
        test_filename_without_group = "test.file.name.with.group.txt"
        warezfile = WarezFile(os.path.join(self.temp_dir,
                                           test_filename_with_group))
        warezfile.remove_group()
        self.assertEqual(os.path.basename(warezfile.filename),
                         test_filename_without_group,
                         msg="Group was not removed")

    def test_fix_show_no_change(self):
        """Test to check properly formatted files don't change
        """
        #Test correctly formatted file (Lowercase)
        test_filename_sxxexx = "test.tv.show.s01e01.resolution.txt"
        warezfile = WarezFile(os.path.join(self.temp_dir,
                                           test_filename_sxxexx))
        warezfile.fix_show()
        self.assertEqual(os.path.basename(warezfile.filename),
                         test_filename_sxxexx,
                         msg="Filename changed")

        #Test correctly formatted file (Uppercase)
        test_filename_sxxexx = "test.tv.show.S01E01.resolution.txt"
        warezfile = WarezFile(os.path.join(self.temp_dir,
                                           test_filename_sxxexx))
        warezfile.fix_show()
        self.assertEqual(os.path.basename(warezfile.filename),
                         test_filename_sxxexx,
                         msg="Filename changed")


        #Test correctly formatted file (Lowercase)
        test_filename_sxxexxexx = "test.tv.show.s01e01e02.resolution.txt"
        warezfile = WarezFile(os.path.join(self.temp_dir,
                                           test_filename_sxxexxexx))
        warezfile.fix_show()
        self.assertEqual(os.path.basename(warezfile.filename),
                         test_filename_sxxexxexx,
                         msg="Filename changed")

        #Test correctly formatted file (Uppercase)
        test_filename_sxxexxexx = "test.tv.show.S01E01E02.resolution.txt"
        warezfile = WarezFile(os.path.join(self.temp_dir,
                                           test_filename_sxxexxexx))
        warezfile.fix_show()
        self.assertEqual(os.path.basename(warezfile.filename),
                         test_filename_sxxexxexx,
                         msg="Filename changed")

        #Test Movie
        test_filename_movie = "test.movie.2015.resolution.txt"
        warezfile = WarezFile(os.path.join(self.temp_dir, test_filename_movie))
        warezfile.fix_show()
        self.assertEqual(os.path.basename(warezfile.filename),
                         test_filename_movie,
                         msg="Movie file changed")

    def test_fix_show_extra_dots(self):
        """Test conversion of sSS.eEE or sSS.eEE.eEE to sSSeEE or sSSeEEeEE
        """
        #Test for 1 episode (Lowercase)
        test_filename_sxxdotexx = "test.tv.show.s01.e01.resolution.txt"
        test_filename_sxxexx = "test.tv.show.s01e01.resolution.txt"
        warezfile = WarezFile(os.path.join(self.temp_dir,
                                           test_filename_sxxdotexx))
        warezfile.fix_show()
        self.assertEqual(os.path.basename(warezfile.filename),
                         test_filename_sxxexx,
                         msg="sXX.eXX was not converted to sXXeXX")

        #Test for 1 episode (Uppercase)
        test_filename_sxxdotexx = "test.tv.show.S01.E01.resolution.txt"
        test_filename_sxxexx = "test.tv.show.S01E01.resolution.txt"
        warezfile = WarezFile(os.path.join(self.temp_dir,
                                           test_filename_sxxdotexx))
        warezfile.fix_show()
        self.assertEqual(os.path.basename(warezfile.filename),
                         test_filename_sxxexx,
                         msg="SXX.EXX was not converted to SXXEXX")

        #Test for 2 episodes (Lowercase)
        test_filename_sxxdotexxdotexx = ("test.tv.show.s01."
                                         "e01.e02.resolution.txt")
        test_filename_sxxexxexx = "test.tv.show.s01e01e02.resolution.txt"
        warezfile = WarezFile(os.path.join(self.temp_dir,
                                           test_filename_sxxdotexxdotexx))
        warezfile.fix_show()
        self.assertEqual(os.path.basename(warezfile.filename),
                         test_filename_sxxexxexx,
                         msg="sXX.eXX.eXX was not converted to sXXeXXeXX")

        #Test for 2 episodes (Uppercase)
        test_filename_sxxdotexxdotexx = ("test.tv.show.S01."
                                         "E01.E02.resolution.txt")
        test_filename_sxxexxexx = "test.tv.show.S01E01E02.resolution.txt"
        warezfile = WarezFile(os.path.join(self.temp_dir,
                                           test_filename_sxxdotexxdotexx))
        warezfile.fix_show()
        self.assertEqual(os.path.basename(warezfile.filename),
                         test_filename_sxxexxexx,
                         msg="sXX.eXX.eXX was not converted to sXXeXXeXX")

    def test_fix_show_numbers_only(self):
        """Test conversion between XXX or XXXXX to sSSeEE or sSSeEEeEE
        """
        #Test for 3 digit number
        test_filename_xxx = "test.tv.show.101.resolution.txt"
        test_filename_sxxexx = "test.tv.show.s01e01.resolution.txt"
        warezfile = WarezFile(os.path.join(self.temp_dir, test_filename_xxx))
        warezfile.fix_show()
        self.assertEqual(os.path.basename(warezfile.filename),
                         test_filename_sxxexx,
                         msg="XXX was not converted to sXXeXX")

        #Test for 5 digit number
        test_filename_xxxxx = "test.tv.show.10102.resolution.txt"
        test_filename_sxxexxexx = "test.tv.show.s01e01e02.resolution.txt"
        warezfile = WarezFile(os.path.join(self.temp_dir, test_filename_xxxxx))
        warezfile.fix_show()
        self.assertEqual(os.path.basename(warezfile.filename),
                         test_filename_sxxexxexx,
                         msg="XXXXX was not converted to sXXeXXeXX")

if __name__ == "__main__":
    unittest.main()
