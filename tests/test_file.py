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
        """Test to check that a groupless file does not get changed lowercase
        """
        test_filename_without_group = "test.file.name.with.no.group.mp4"

        warezfile = WarezFile(os.path.join(self.temp_dir,
                                           test_filename_without_group.lower()))
        warezfile.remove_group()
        self.assertEqual(os.path.basename(warezfile.filename),
                         test_filename_without_group,
                         msg="Filename changed")
        warezfile = WarezFile(os.path.join(self.temp_dir,
                                           test_filename_without_group.upper()))
        warezfile.remove_group()
        self.assertEqual(os.path.basename(warezfile.filename),
                         test_filename_without_group.upper(),
                         msg="Filename changed")

    def test_remove_group_with_group(self):
        """Test removal of scene group lowercase
        """
        test_filename_with_group = "test.file.name.with.group-groupname.mp4"
        test_filename_without_group = "test.file.name.with.group.mp4"
        warezfile = WarezFile(os.path.join(self.temp_dir,
                                           test_filename_with_group.lower()))
        warezfile.remove_group()
        self.assertEqual(os.path.basename(warezfile.filename),
                         test_filename_without_group.lower(),
                         msg="Group was not removed")
        warezfile = WarezFile(os.path.join(self.temp_dir,
                                           test_filename_with_group.upper()))
        warezfile.remove_group()
        self.assertEqual(os.path.basename(warezfile.filename),
                         test_filename_without_group.upper(),
                         msg="Group was not removed")

    def test_fix_show_no_change_one_episode(self):
        """Test to check properly formatted lowercase files don't change
        """
        #Test correctly formatted file
        test_filename = "test.tv.show.s01e01.resolution.mp4"
        warezfile = WarezFile(os.path.join(self.temp_dir,
                                           test_filename.lower()))
        warezfile.fix_show()
        self.assertEqual(os.path.basename(warezfile.filename),
                         test_filename.lower(),
                         msg="Filename changed")
        warezfile = WarezFile(os.path.join(self.temp_dir,
                                           test_filename.upper()))
        warezfile.fix_show()
        self.assertEqual(os.path.basename(warezfile.filename),
                         test_filename.upper(),
                         msg="Filename changed")

    def test_fix_show_no_change_two_episodes(self):
        """Test to check properly formatted lowercase files don't change
        """
        #Test correctly formatted file
        test_filename = "test.tv.show.s01e01e02.resolution.mp4"
        warezfile = WarezFile(os.path.join(self.temp_dir,
                                           test_filename.lower()))
        warezfile.fix_show()
        self.assertEqual(os.path.basename(warezfile.filename),
                         test_filename.lower(),
                         msg="Filename changed")
        warezfile = WarezFile(os.path.join(self.temp_dir,
                                           test_filename.upper()))
        warezfile.fix_show()
        self.assertEqual(os.path.basename(warezfile.filename),
                         test_filename.upper(),
                         msg="Filename changed")

    def test_fix_show_not_show(self):
        """Test to check non-shows don't get modified
        """
        test_filename = "test.movie.2015.resolution.mp4"
        warezfile = WarezFile(os.path.join(self.temp_dir,
                                           test_filename.lower()))
        warezfile.fix_show()
        self.assertEqual(os.path.basename(warezfile.filename),
                         test_filename.lower(),
                         msg="Movie file changed")
        warezfile = WarezFile(os.path.join(self.temp_dir,
                                           test_filename.upper()))
        warezfile.fix_show()
        self.assertEqual(os.path.basename(warezfile.filename),
                         test_filename.upper(),
                         msg="Movie file changed")

    def test_fix_show_extra_dots_one_episode(self):
        """Test conversion of sSS.eEE to sSSeEE
        """
        #Test for 1 episode
        test_filename_dot = "test.tv.show.s01.e01.resolution.mp4"
        test_filename = "test.tv.show.s01e01.resolution.mp4"
        warezfile = WarezFile(os.path.join(self.temp_dir,
                                           test_filename_dot.lower()))
        warezfile.fix_show()
        self.assertEqual(os.path.basename(warezfile.filename),
                         test_filename.lower(),
                         msg="sSS.eEE was not converted to sSSeEE")
        warezfile = WarezFile(os.path.join(self.temp_dir,
                                           test_filename_dot.upper()))
        warezfile.fix_show()
        self.assertEqual(os.path.basename(warezfile.filename),
                         test_filename.upper(),
                         msg="sSS.eEE was not converted to sSSeEE")

    def test_fix_show_extra_dots_two_episodes(self):
        """Test conversion of sSS.eEE.eEE to sSSeEEeEE
        """
        test_filename_dot = ("test.tv.show.s01."
                                         "e01.e02.resolution.mp4")
        test_filename = "test.tv.show.s01e01e02.resolution.mp4"
        warezfile = WarezFile(os.path.join(self.temp_dir,
                                           test_filename_dot.lower()))
        warezfile.fix_show()
        self.assertEqual(os.path.basename(warezfile.filename),
                         test_filename.lower(),
                         msg="sSS.eEE.eEE was not converted to sSSeEEeEE")
        warezfile = WarezFile(os.path.join(self.temp_dir,
                                           test_filename_dot.upper()))
        warezfile.fix_show()
        self.assertEqual(os.path.basename(warezfile.filename),
                         test_filename.upper(),
                         msg="sSS.eEE.eEE was not converted to sSSeEEeEE")

    def test_fix_show_numbers_only_one_episode(self):
        """Test conversion of SEE to sSSeEE
        """
        test_filename_number = "test.tv.show.101.resolution.mp4"
        test_filename = "test.tv.show.s01e01.resolution.mp4"
        warezfile = WarezFile(os.path.join(self.temp_dir, test_filename_number))
        warezfile.fix_show()
        self.assertEqual(os.path.basename(warezfile.filename),
                         test_filename,
                         msg="SEE was not converted to s0SeEE")

    def test_fix_show_numbers_only_two_episodes(self):
        """Test conversion of SEEEE to sSSeEEeEE
        """
        test_filename_number = "test.tv.show.10102.resolution.mp4"
        test_filename = "test.tv.show.s01e01e02.resolution.mp4"
        warezfile = WarezFile(os.path.join(self.temp_dir, test_filename_number))
        warezfile.fix_show()
        self.assertEqual(os.path.basename(warezfile.filename),
                         test_filename,
                         msg="SEEEE was not converted to s0SeEEeSS")

if __name__ == "__main__":
    unittest.main()
