"""
author: Rahul Mohandas
"""
import unittest
import os
import errno
import shutil
import tempfile

from wareztools.video import Video

class FakeScraper(object):

    def __init__(self, api_key=None):
        pass

    def get_show_id(self, name):
        return 1

    def validate_show(self, name):
        return True

    def validate_show_season(self, name, season):
        return True

    def validate_show_episode(self, name, season, episode):
        return True

    def get_movie_id(self, name):
        return 1

    def validate_movie(self, name):
        return True

class TestVideo(unittest.TestCase):
    """Test the Video class
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
        test_filenames = ["test.file.name.with.no.group.mp4"]

        for test_filename in test_filenames:
            warezfile = Video(os.path.join(self.temp_dir,
                                           test_filename.lower()))
            warezfile.remove_group()
            self.assertEqual(os.path.basename(warezfile.filename),
                             test_filename.lower(),
                             "{0} changed to {1}".format(test_filename.lower(),
                                                         warezfile.filename))
            warezfile = Video(os.path.join(self.temp_dir,
                                           test_filename.upper()))
            warezfile.remove_group()
            self.assertEqual(os.path.basename(warezfile.filename),
                             test_filename.upper(),
                             "{0} changed to {1}".format(test_filename.upper(),
                                                         warezfile.filename))

    def test_remove_group_with_group(self):
        """Test removal of scene group
        """
        test_filenames = [{"test":"test.file.name.with.group-groupname.mp4",
                           "correct":"test.file.name.with.group.mp4"}]
        for test_filename in test_filenames:
            warezfile = Video(os.path.join(self.temp_dir,
                                           test_filename["test"].lower()))
            warezfile.remove_group()
            self.assertEqual(os.path.basename(warezfile.filename),
                             test_filename["correct"].lower(),
                             "Group was not removed")
            warezfile = Video(os.path.join(self.temp_dir,
                                           test_filename["test"].upper()))
            warezfile.remove_group()
            self.assertEqual(os.path.basename(warezfile.filename),
                             test_filename["correct"].upper(),
                             "Group was not removed")

    def test_fix_season_episode_format_no_change_one_episode(self):
        """Test to check properly formatted files do not change
        """
        #Test correctly formatted file
        test_filenames = ["test.tv.s01e01.resolution.mp4"]
        for test_filename in test_filenames:
            warezfile = Video(os.path.join(self.temp_dir,
                                           test_filename.lower()))
            warezfile._Video__fix_season_episode_format()
            self.assertEqual(os.path.basename(warezfile.filename),
                             test_filename.lower(),
                             "{0} changed to {1}".format(test_filename.lower(),
                                                         warezfile.filename))
            warezfile = Video(os.path.join(self.temp_dir,
                                           test_filename.upper()))
            warezfile._Video__fix_season_episode_format()
            self.assertEqual(os.path.basename(warezfile.filename),
                             test_filename.upper(),
                             "{0} changed to {1}".format(test_filename.upper(),
                                                         warezfile.filename))

    def test_fix_season_episode_format_no_change_two_episodes(self):
        """Test to check properly formatted files do not change
        """
        #Test correctly formatted file
        test_filenames = ["test.tv.s01e01e02.resolution.mp4"]
        for test_filename in test_filenames:
            warezfile = Video(os.path.join(self.temp_dir,
                                           test_filename.lower()))
            warezfile._Video__fix_season_episode_format()
            self.assertEqual(os.path.basename(warezfile.filename),
                             test_filename.lower(),
                             "{0} changed to {1}".format(test_filename.lower(),
                                                         warezfile.filename))
            warezfile = Video(os.path.join(self.temp_dir,
                                           test_filename.upper()))
            warezfile._Video__fix_season_episode_format()
            self.assertEqual(os.path.basename(warezfile.filename),
                             test_filename.upper(),
                             "{0} changed to {1}".format(test_filename.upper(),
                                                         warezfile.filename))

    def test_fix_season_episode_format_not_show(self):
        """Test to check non-shows don't get modified
        """
        test_filenames = ["test.movie.2015.resolution.mp4"]
        for test_filename in test_filenames:
            warezfile = Video(os.path.join(self.temp_dir,
                                           test_filename.lower()))
            warezfile._Video__fix_season_episode_format()
            self.assertEqual(os.path.basename(warezfile.filename),
                             test_filename.lower(),
                             "{0} changed to {1}".format(test_filename.lower(),
                                                         warezfile.filename))
            warezfile = Video(os.path.join(self.temp_dir,
                                           test_filename.upper()))
            warezfile._Video__fix_season_episode_format()
            self.assertEqual(os.path.basename(warezfile.filename),
                             test_filename.upper(),
                             "{0} changed to {1}".format(test_filename.upper(),
                                                         warezfile.filename))

    def test_fix_season_episode_format_extra_dots_one_episode(self):
        """Test conversion of sSS.eEE to sSSeEE
        """
        test_filenames = [{"test":"test.tv.s01.e01.resolution.mp4",
                           "correct":"test.tv.s01e01.resolution.mp4"}]
        for test_filename in test_filenames:
            warezfile = Video(os.path.join(self.temp_dir,
                                           test_filename["test"].lower()))
            warezfile._Video__fix_season_episode_format()
            self.assertEqual(os.path.basename(warezfile.filename),
                             test_filename["correct"].lower(),
                             msg="sSS.eEE was not converted to sSSeEE")
            warezfile = Video(os.path.join(self.temp_dir,
                                           test_filename["test"].upper()))
            warezfile._Video__fix_season_episode_format()
            self.assertEqual(os.path.basename(warezfile.filename),
                             test_filename["correct"].upper(),
                             msg="sSS.eEE was not converted to sSSeEE")

    def test_fix_season_episode_format_extra_dots_two_episodes(self):
        """Test conversion of sSS.eEE.eEE to sSSeEEeEE
        """
        test_filenames = [{"test":"test.tv.s01.e01.e02.resolution.mp4",
                           "correct":"test.tv.s01e01e02.resolution.mp4"}]
        for test_filename in test_filenames:
            warezfile = Video(os.path.join(self.temp_dir,
                                           test_filename["test"].lower()))
            warezfile._Video__fix_season_episode_format()
            self.assertEqual(os.path.basename(warezfile.filename),
                             test_filename["correct"].lower(),
                             msg="sSS.eEE.eEE was not converted to sSSeEEeEE")
            warezfile = Video(os.path.join(self.temp_dir,
                                           test_filename["test"].upper()))
            warezfile._Video__fix_season_episode_format()
            self.assertEqual(os.path.basename(warezfile.filename),
                             test_filename["correct"].upper(),
                             msg="sSS.eEE.eEE was not converted to sSSeEEeEE")

    def test_fix_season_episode_format_numbers_only_one_episode(self):
        """Test conversion of SEE to sSSeEE
        """
        test_filenames = [{"test":"test.tv.101.resolution.mp4",
                           "correct":"test.tv.s01e01.resolution.mp4"}]
        for test_filename in test_filenames:
            warezfile = Video(os.path.join(self.temp_dir,
                                           test_filename["test"]))
            warezfile._Video__fix_season_episode_format()
            self.assertEqual(os.path.basename(warezfile.filename),
                             test_filename["correct"],
                             msg="SEE was not converted to s0SeEE")

    def test_fix_season_episode_format_numbers_only_two_episodes(self):
        """Test conversion of SEEEE to sSSeEEeEE
        """
        test_filenames = [{"test":"test.tv.10102.resolution.mp4",
                           "correct":"test.tv.s01e01e02.resolution.mp4"}]
        for test_filename in test_filenames:
            warezfile = Video(os.path.join(self.temp_dir,
                              test_filename["test"]))
            warezfile._Video__fix_season_episode_format()
            self.assertEqual(os.path.basename(warezfile.filename),
                             test_filename["correct"],
                             msg="SEEEE was not converted to s0SeEEeEE")

    def test_remove_proper_no_change(self):
        """Test to check that a file with no proper does not change
        """
        test_filenames = ["test.tv.s01e01.resolution.mp4"]
        for test_filename in test_filenames:
            warezfile = Video(os.path.join(self.temp_dir,
                                           test_filename.lower()))
            warezfile.remove_proper()
            self.assertEqual(os.path.basename(warezfile.filename),
                             test_filename.lower(),
                             "{0} changed to {1}".format(test_filename.lower(),
                             warezfile.filename))
            warezfile = Video(os.path.join(self.temp_dir,
                                           test_filename.upper()))
            warezfile.remove_proper()
            self.assertEqual(os.path.basename(warezfile.filename),
                             test_filename.upper(),
                             "{0} changed to {1}".format(test_filename.upper(),
                             warezfile.filename))

    def test_remove_proper_with_proper(self):
        """Test the removal of proper in filename
        """
        test_filenames = [{"test":"test.tv.s01e01.proper.resolution.mp4",
                           "correct":"test.tv.s01e01.resolution.mp4"}]
        for test_filename in test_filenames:
            warezfile = Video(os.path.join(self.temp_dir,
                                           test_filename["test"].lower()))
            warezfile.remove_proper()
            self.assertEqual(os.path.basename(warezfile.filename),
                             test_filename["correct"].lower(),
                             msg="proper was not removed")
            warezfile = Video(os.path.join(self.temp_dir,
                                           test_filename["test"].upper()))
            warezfile.remove_proper()
            self.assertEqual(os.path.basename(warezfile.filename),
                             test_filename["correct"].upper(),
                             msg="PROPER was not removed")

    def test_remove_repack_no_change(self):
        """Test to check that a file with no repack does not change
        """
        test_filenames = ["test.tv.s01e01.resolution.mp4"]
        for test_filename in test_filenames:
            warezfile = Video(os.path.join(self.temp_dir,
                                           test_filename.lower()))
            warezfile.remove_repack()
            self.assertEqual(os.path.basename(warezfile.filename),
                             test_filename.lower(),
                             "{0} changed to {1}".format(test_filename.lower(),
                             warezfile.filename))
            warezfile = Video(os.path.join(self.temp_dir,
                                           test_filename.upper()))
            warezfile.remove_repack()
            self.assertEqual(os.path.basename(warezfile.filename),
                             test_filename.upper(),
                             "{0} changed to {1}".format(test_filename.upper(),
                             warezfile.filename))

    def test_remove_repack_with_repack(self):
        """Test the removal of repack in filename
        """
        test_filenames = [{"test":"test.tv.s01e01.repack.resolution.mp4",
                           "correct":"test.tv.s01e01.resolution.mp4"}]
        for test_filename in test_filenames:
            warezfile = Video(os.path.join(self.temp_dir,
                                           test_filename["test"].lower()))
            warezfile.remove_repack()
            self.assertEqual(os.path.basename(warezfile.filename),
                             test_filename["correct"].lower(),
                             msg="repack was not removed")
            warezfile = Video(os.path.join(self.temp_dir,
                                           test_filename["test"].upper()))
            warezfile.remove_repack()
            self.assertEqual(os.path.basename(warezfile.filename),
                             test_filename["correct"].upper(),
                             msg="REPACK was not removed")

    def test_remove_internal_no_change(self):
        """Test to check that a file with no internal does not change
        """
        test_filenames = ["test.tv.s01e01.resolution.mp4"]
        for test_filename in test_filenames:
            warezfile = Video(os.path.join(self.temp_dir,
                                           test_filename.lower()))
            warezfile.remove_internal()
            self.assertEqual(os.path.basename(warezfile.filename),
                             test_filename.lower(),
                             "{0} changed to {1}".format(test_filename.lower(),
                             warezfile.filename))
            warezfile = Video(os.path.join(self.temp_dir,
                                           test_filename.upper()))
            warezfile.remove_internal()
            self.assertEqual(os.path.basename(warezfile.filename),
                             test_filename.upper(),
                             "{0} changed to {1}".format(test_filename.upper(),
                             warezfile.filename))

    def test_remove_internal_with_internal(self):
        """Test the removal of internal in filename
        """
        test_filenames = [{"test":"test.tv.s01e01.internal.resolution.mp4",
                           "correct":"test.tv.s01e01.resolution.mp4"}]
        for test_filename in test_filenames:
            warezfile = Video(os.path.join(self.temp_dir,
                                           test_filename["test"].lower()))
            warezfile.remove_internal()
            self.assertEqual(os.path.basename(warezfile.filename),
                             test_filename["correct"].lower(),
                             msg="internal was not removed")
            warezfile = Video(os.path.join(self.temp_dir,
                                           test_filename["test"].upper()))
            warezfile.remove_internal()
            self.assertEqual(os.path.basename(warezfile.filename),
                             test_filename["correct"].upper(),
                             msg="INTERNAL was not removed")

    def test_move_to_movie(self):
        """Test the move to movie directory
        """
        test_filenames = [{"test":"test.movie.resolution.mp4",
                           "correct":"movie/test.movie.resolution.mp4"}]
        for test_filename in test_filenames:
            warezfile = Video(os.path.join(self.temp_dir,
                                           test_filename["test"].lower()))
            warezfile.move_to_movie()
            self.assertEqual(os.path.join(warezfile.path, warezfile.filename),
                             os.path.join(self.temp_dir,
                                          test_filename["correct"]),
                             msg="not moved to movie folder")

    def test_move_to_tv(self):
        """Test the move to tv directory
        """
        test_filenames = [{"test":"test.tv.s01e01.resolution.mp4",
                           "correct":"tv/test.tv.s01e01.resolution.mp4"}]
        for test_filename in test_filenames:
            warezfile = Video(os.path.join(self.temp_dir,
                                           test_filename["test"].lower()))
            warezfile.move_to_tv()
            self.assertEqual(os.path.join(warezfile.path, warezfile.filename),
                             os.path.join(self.temp_dir,
                                          test_filename["correct"]),
                             msg="not moved to tv folder")

    def test_get_show_info_no_show(self):
        """Test getting show info when no show info is present
        """
        test_filenames = [{"test":"test.movie.resolution.mp4",
                           "correct":(None, None, [])}]
        for test_filename in test_filenames:
            warezfile = Video(os.path.join(self.temp_dir,
                                           test_filename["test"].lower()))
            warezfile.db = FakeScraper()
            show_info = warezfile.get_show_info()
            self.assertEqual(show_info,
                             test_filename["correct"],
                             msg="Show info found")

    def test_get_show_info_show(self):
        """Test getting show info when show info is present
        """
        test_filenames = [{"test":"test.tv.s01.e01.resolution.mp4",
                           "correct":("test.tv", "01", ["01"])},
                          {"test":"test.tv.s01.e01.e02.resolution.mp4",
                           "correct":("test.tv", "01", ["01", "02"])}]
        for test_filename in test_filenames:
            warezfile = Video(os.path.join(self.temp_dir,
                                           test_filename["test"].lower()))
            warezfile.db = FakeScraper()
            show_info = warezfile.get_show_info()
            self.assertEqual(show_info,
                             test_filename["correct"],
                             msg="No show info found")

    def test_all_functions(self):
        """Test all functions together
        """
        test_filenames = [{"test":("test.tv.s01.e01."
                                   "resolution.internal-GROUP.mp4"),
                           "correct":"test.tv.s01e01.resolution.mp4"},
                          {"test":("test.tv.s01.e01."
                                   "resolution.repack-GROUP.mp4"),
                           "correct":"test.tv.s01e01.resolution.mp4"},
                          {"test":("test.tv.s01.e01."
                                   "resolution.proper-GROUP.mp4"),
                           "correct":"test.tv.s01e01.resolution.mp4"},
                          {"test":("test.tv.s01.e01.e02."
                                   "resolution.internal-GROUP.mp4"),
                           "correct":"test.tv.s01e01e02.resolution.mp4"},
                          {"test":("test.tv.s01.e01.e02."
                                   "resolution.repack-GROUP.mp4"),
                           "correct":"test.tv.s01e01e02.resolution.mp4"},
                          {"test":("test.tv.s01.e01.e02."
                                   "resolution.proper-GROUP.mp4"),
                           "correct":"test.tv.s01e01e02.resolution.mp4"},
                          {"test":("test.tv.101."
                                   "resolution.internal-GROUP.mp4"),
                           "correct":"test.tv.s01e01.resolution.mp4"},
                          {"test":("test.tv.101."
                                   "resolution.repack-GROUP.mp4"),
                           "correct":"test.tv.s01e01.resolution.mp4"},
                          {"test":("test.tv.101."
                                   "resolution.proper-GROUP.mp4"),
                           "correct":"test.tv.s01e01.resolution.mp4"},
                          {"test":("test.tv.10102."
                                   "resolution.internal-GROUP.mp4"),
                           "correct":"test.tv.s01e01e02.resolution.mp4"},
                          {"test":("test.tv.10102."
                                   "resolution.repack-GROUP.mp4"),
                           "correct":"test.tv.s01e01e02.resolution.mp4"},
                          {"test":("test.tv.10102."
                                   "resolution.proper-GROUP.mp4"),
                           "correct":"test.tv.s01e01e02.resolution.mp4"},]
        for test_filename in test_filenames:
            warezfile = Video(os.path.join(self.temp_dir,
                                           test_filename["test"].lower()))
            warezfile.remove_group()
            warezfile.remove_internal()
            warezfile.remove_proper()
            warezfile.remove_repack()
            warezfile._Video__fix_season_episode_format()
            self.assertEqual(os.path.join(warezfile.path, warezfile.filename),
                             os.path.join(self.temp_dir,
                                          test_filename["correct"]),
                             "{0} changed to {1}".format(test_filename,
                             warezfile.filename))

if __name__ == "__main__":
    unittest.main()
