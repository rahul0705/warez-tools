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

    def test_remove_group_no_change_lowercase(self):
        """Test to check that a groupless file does not get changed lowercase
        """
        test_filename_without_group = "test.file.name.with.no.group.mp4"
        warezfile = WarezFile(os.path.join(self.temp_dir,
                                           test_filename_without_group))
        warezfile.remove_group()
        self.assertEqual(os.path.basename(warezfile.filename),
                         test_filename_without_group,
                         msg="Filename changed")

    def test_remove_group_no_change_uppercase(self):
        """Test to check that a groupless file does not get changed uppercase
        """
        test_filename_without_group = "TEST.FILE.NAME.WITH.NO.GROUP.MP4"
        warezfile = WarezFile(os.path.join(self.temp_dir,
                                           test_filename_without_group))
        warezfile.remove_group()
        self.assertEqual(os.path.basename(warezfile.filename),
                         test_filename_without_group,
                         msg="Filename changed")

    def test_remove_group_with_group_lowercase(self):
        """Test removal of scene group lowercase
        """
        test_filename_with_group = "test.file.name.with.group-groupname.mp4"
        test_filename_without_group = "test.file.name.with.group.mp4"
        warezfile = WarezFile(os.path.join(self.temp_dir,
                                           test_filename_with_group))
        warezfile.remove_group()
        self.assertEqual(os.path.basename(warezfile.filename),
                         test_filename_without_group,
                         msg="Group was not removed")

    def test_remove_group_with_group_uppercase(self):
        """Test removal of scene group uppercase
        """
        test_filename_with_group = "TEST.FILE.NAME.WITH.GROUP-GROUPNAME.MP4"
        test_filename_without_group = "TEST.FILE.NAME.WITH.GROUP.MP4"
        warezfile = WarezFile(os.path.join(self.temp_dir,
                                           test_filename_with_group))
        warezfile.remove_group()
        self.assertEqual(os.path.basename(warezfile.filename),
                         test_filename_without_group,
                         msg="Group was not removed")

    def test_fix_show_no_change_lowercase(self):
        """Test to check properly formatted lowercase files don't change
        """
        #Test correctly formatted file (Lowercase)
        test_filename_sxxexx = "test.tv.show.s01e01.resolution.mp4"
        warezfile = WarezFile(os.path.join(self.temp_dir,
                                           test_filename_sxxexx))
        warezfile.fix_show()
        self.assertEqual(os.path.basename(warezfile.filename),
                         test_filename_sxxexx,
                         msg="Filename changed")

        #Test correctly formatted file (Lowercase)
        test_filename_sxxexxexx = "test.tv.show.s01e01e02.resolution.mp4"
        warezfile = WarezFile(os.path.join(self.temp_dir,
                                           test_filename_sxxexxexx))
        warezfile.fix_show()
        self.assertEqual(os.path.basename(warezfile.filename),
                         test_filename_sxxexxexx,
                         msg="Filename changed")

        #Test Movie
        test_filename_movie = "test.movie.2015.resolution.mp4"
        warezfile = WarezFile(os.path.join(self.temp_dir, test_filename_movie))
        warezfile.fix_show()
        self.assertEqual(os.path.basename(warezfile.filename),
                         test_filename_movie,
                         msg="Movie file changed")

    def test_fix_show_no_change_uppercase(self):
        """Test to check properly formatted uppercase files don't change
        """
        #Test correctly formatted file
        test_filename_sxxexx = "TEST.TV.SHOW.S01E01.RESOLUTION.mp4"
        warezfile = WarezFile(os.path.join(self.temp_dir,
                                           test_filename_sxxexx))
        warezfile.fix_show()
        self.assertEqual(os.path.basename(warezfile.filename),
                         test_filename_sxxexx,
                         msg="Filename changed")

        #Test correctly formatted file
        test_filename_sxxexxexx = "TEST.TV.SHOW.S01E01E02.RESOLUTION.mp4"
        warezfile = WarezFile(os.path.join(self.temp_dir,
                                           test_filename_sxxexxexx))
        warezfile.fix_show()
        self.assertEqual(os.path.basename(warezfile.filename),
                         test_filename_sxxexxexx,
                         msg="Filename changed")

        #Test Movie
        test_filename_movie = "TEST.MOVIE.2015.RESOLUTION.MP4"
        warezfile = WarezFile(os.path.join(self.temp_dir, test_filename_movie))
        warezfile.fix_show()
        self.assertEqual(os.path.basename(warezfile.filename),
                         test_filename_movie,
                         msg="Movie file changed")

    def test_fix_show_extra_dots_lowercase(self):
        """Test conversion of sSS.eEE or sSS.eEE.eEE to sSSeEE or sSSeEEeEE
        """
        #Test for 1 episode
        test_filename_sxxdotexx = "test.tv.show.s01.e01.resolution.mp4"
        test_filename_sxxexx = "test.tv.show.s01e01.resolution.mp4"
        warezfile = WarezFile(os.path.join(self.temp_dir,
                                           test_filename_sxxdotexx))
        warezfile.fix_show()
        self.assertEqual(os.path.basename(warezfile.filename),
                         test_filename_sxxexx,
                         msg="sSS.eEE was not converted to sSSeEE")

        #Test for 2 episodes
        test_filename_sxxdotexxdotexx = ("test.tv.show.s01."
                                         "e01.e02.resolution.mp4")
        test_filename_sxxexxexx = "test.tv.show.s01e01e02.resolution.mp4"
        warezfile = WarezFile(os.path.join(self.temp_dir,
                                           test_filename_sxxdotexxdotexx))
        warezfile.fix_show()
        self.assertEqual(os.path.basename(warezfile.filename),
                         test_filename_sxxexxexx,
                         msg="sSS.eEE.eEE was not converted to sSSeEEeEE")

    def test_fix_show_extra_dots_uppercase(self):
        """Test conversion of sSS.eEE or sSS.eEE.eEE to sSSeEE or sSSeEEeEE
        """
        #Test for 1 episode
        test_filename_sxxdotexx = "test.tv.show.S01.E01.resolution.mp4"
        test_filename_sxxexx = "test.tv.show.S01E01.resolution.mp4"
        warezfile = WarezFile(os.path.join(self.temp_dir,
                                           test_filename_sxxdotexx))
        warezfile.fix_show()
        self.assertEqual(os.path.basename(warezfile.filename),
                         test_filename_sxxexx,
                         msg="SSS.EEE was not converted to SSSEEE")

        #Test for 2 episodes
        test_filename_sxxdotexxdotexx = ("test.tv.show.S01."
                                         "E01.E02.resolution.mp4")
        test_filename_sxxexxexx = "test.tv.show.S01E01E02.resolution.mp4"
        warezfile = WarezFile(os.path.join(self.temp_dir,
                                           test_filename_sxxdotexxdotexx))
        warezfile.fix_show()
        self.assertEqual(os.path.basename(warezfile.filename),
                         test_filename_sxxexxexx,
                         msg="sSS.eEE.eEE was not converted to sSSeEEeEE")

    def test_fix_show_numbers_only(self):
        """Test conversion of SEE or SEEEE to sSSeEE or sSSeEEeEE
        """
        #Test for 3 digit number
        test_filename_xxx = "test.tv.show.101.resolution.mp4"
        test_filename_sxxexx = "test.tv.show.s01e01.resolution.mp4"
        warezfile = WarezFile(os.path.join(self.temp_dir, test_filename_xxx))
        warezfile.fix_show()
        self.assertEqual(os.path.basename(warezfile.filename),
                         test_filename_sxxexx,
                         msg="SEE was not converted to s0SeEE")

        #Test for 5 digit number
        test_filename_xxxxx = "test.tv.show.10102.resolution.mp4"
        test_filename_sxxexxexx = "test.tv.show.s01e01e02.resolution.mp4"
        warezfile = WarezFile(os.path.join(self.temp_dir, test_filename_xxxxx))
        warezfile.fix_show()
        self.assertEqual(os.path.basename(warezfile.filename),
                         test_filename_sxxexxexx,
                         msg="SEEEE was not converted to s0SeEEeSS")

if __name__ == "__main__":
    unittest.main()
