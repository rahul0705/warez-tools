"""
author: Rahul Mohandas
"""
import unittest
import os
import errno
import shutil
import tempfile
import logging

import wareztools.video

class FakeScraper(object):
    ret = True

    def __init__(self, api_key=None):
        pass

    def get_show_id(self, name):
        return 1

    def validate_show(self, name):
        return FakeScraper.ret

    def validate_show_season(self, name, season):
        return FakeScraper.ret

    def validate_show_episode(self, name, season, episode):
        return FakeScraper.ret

    def get_movie_id(self, name):
        return 1

    def validate_movie(self, name):
        return FakeScraper.ret

class TestVideo(unittest.TestCase):
    """Test the Video class
    """

    def setUp(self):
        wareztools.scrapers.themoviedb.TheMovieDB = FakeScraper
        # Create short hand for videofile module
        self.video = wareztools.video.Video
        try:
            # Create temp dir so we can test changing dirs
            self.temp_dir = tempfile.mkdtemp()
        except:
            try:
                # If we fail at making any temp dir clean yourself up
                shutil.rmtree(self.temp_dir)
            except OSError as exc:
                if exc.errno != errno.ENOENT:
                    raise

    def tearDown(self):
        try:
            # Clean temp dir up
            shutil.rmtree(self.temp_dir)
        except OSError as exc:
            if exc.errno != errno.ENOENT:
                raise

    def test_remove_group_no_group(self):
        """Test to check that a groupless file does not get changed
        """
        test_filenames = ["test.file.name.with.no.group.mp4"]

        for test_filename in test_filenames:
            #----LOWER CASE TEST CASE----#
            test_file = os.path.join(self.temp_dir, test_filename.lower())
            videofile = self.video(test_file)
            videofile.remove_group()
            self.assertEqual(videofile.file, test_file)

            #----UPPER CASE TEST CASE----#
            test_file = os.path.join(self.temp_dir, test_filename.upper())
            videofile = self.video(test_file)
            videofile.remove_group()
            self.assertEqual(videofile.file, test_file)

    def test_remove_group_with_group(self):
        """Test removal of scene group
        """
        test_filenames = [
                             {
                               'test' : 'test.file.name.with.group-groupname.mp4',
                               'correct' : 'test.file.name.with.group.mp4'
                             }
                         ]

        for test_filename in test_filenames:
            #----LOWER CASE TEST CASE----#
            test_file = os.path.join(self.temp_dir,
                                     test_filename['test'].lower())
            correct_file = os.path.join(self.temp_dir,
                                        test_filename['correct'].lower())
            with open(test_file, 'w'):
                pass
            videofile = self.video(test_file)
            videofile.remove_group()
            self.assertEqual(videofile.file, correct_file)
            os.remove(correct_file)

            #----UPPER CASE TEST CASE----#
            test_file = os.path.join(self.temp_dir,
                                     test_filename['test'].upper())
            correct_file = os.path.join(self.temp_dir,
                                        test_filename['correct'].upper())
            with open(test_file, 'w'):
                pass
            videofile = self.video(test_file)
            videofile.remove_group()
            self.assertEqual(videofile.file, correct_file)
            os.remove(correct_file)

    def test_fix_season_episode_format_no_change_one_episode(self):
        """Test to check properly formatted files do not change
        """
        #Test correctly formatted file
        test_filenames = ["test.tv.s01e01.resolution.mp4",
                          "test.tv.with.year.2018.s01e01.resolution.mp4"]

        for test_filename in test_filenames:
            #----LOWER CASE TEST CASE----#
            test_file = os.path.join(self.temp_dir, test_filename.lower())
            videofile = self.video(test_file)
            videofile._Video__fix_season_episode_format()
            self.assertEqual(videofile.file, test_file)

            #----UPPER CASE TEST CASE----#
            test_file = os.path.join(self.temp_dir, test_filename.upper())
            videofile = self.video(test_file)
            videofile._Video__fix_season_episode_format()
            self.assertEqual(videofile.file, test_file)

    def test_fix_season_episode_format_no_change_two_episodes(self):
        """Test to check properly formatted files do not change
        """
        #Test correctly formatted file
        test_filenames = ["test.tv.s01e01e02.resolution.mp4",
                          "test.tv.with.year.2018.s01e01e02.resolution.mp4"]

        for test_filename in test_filenames:
            #----LOWER CASE TEST CASE----#
            test_file = os.path.join(self.temp_dir, test_filename.lower())
            videofile = self.video(test_file)
            videofile._Video__fix_season_episode_format()
            self.assertEqual(videofile.file, test_file)

            #----UPPER CASE TEST CASE----#
            test_file = os.path.join(self.temp_dir, test_filename.upper())
            videofile = self.video(test_file)
            videofile._Video__fix_season_episode_format()
            self.assertEqual(videofile.file, test_file)

    def test_fix_season_episode_format_not_show(self):
        """Test to check non-shows don't get modified
        """
        test_filenames = ["test.movie.2015.resolution.mp4"]

        for test_filename in test_filenames:
            #----LOWER CASE TEST CASE----#
            test_file = os.path.join(self.temp_dir, test_filename.lower())
            videofile = self.video(test_file)
            videofile._Video__fix_season_episode_format()
            self.assertEqual(videofile.file, test_file)

            #----UPPER CASE TEST CASE----#
            test_file = os.path.join(self.temp_dir, test_filename.upper())
            videofile = self.video(test_file)
            videofile._Video__fix_season_episode_format()
            self.assertEqual(videofile.file, test_file)

    def test_fix_season_episode_format_extra_dots_one_episode(self):
        """Test conversion of sSS.eEE to sSSeEE
        """
        test_filenames = [
                           {
                             'test' : 'test.tv.s01.e01.resolution.mp4',
                             'correct' : 'test.tv.s01e01.resolution.mp4'
                           },
                           {
                             'test' : 'test.tv.with.year.2018.s01.e01.resolution.mp4',
                             'correct' : 'test.tv.with.year.2018.s01e01.resolution.mp4'
                           }
                         ]

        for test_filename in test_filenames:
            #----LOWER CASE TEST CASE----#
            test_file = os.path.join(self.temp_dir,
                                     test_filename['test'].lower())
            correct_file = os.path.join(self.temp_dir,
                                        test_filename['correct'].lower())
            with open(test_file, 'w'):
                pass
            videofile = self.video(test_file)
            videofile._Video__fix_season_episode_format()
            self.assertEqual(videofile.file, correct_file)
            os.remove(correct_file)

            #----UPPER CASE TEST CASE----#
            test_file = os.path.join(self.temp_dir,
                                     test_filename['test'].upper())
            correct_file = os.path.join(self.temp_dir,
                                        test_filename['correct'].upper())
            with open(test_file, 'w'):
                pass
            videofile = self.video(test_file)
            videofile._Video__fix_season_episode_format()
            self.assertEqual(videofile.file, correct_file)
            os.remove(correct_file)

    def test_fix_season_episode_format_extra_dots_two_episodes(self):
        """Test conversion of sSS.eEE.eEE to sSSeEEeEE
        """
        test_filenames = [
                           {
                             'test' : 'test.tv.s01.e01.e02.resolution.mp4',
                             'correct' : 'test.tv.s01e01e02.resolution.mp4'
                           },
                           {
                             'test' : 'test.tv.with.year.2018.s01.e01.e02.resolution.mp4',
                             'correct' : 'test.tv.with.year.2018.s01e01e02.resolution.mp4'
                           }
                         ]

        for test_filename in test_filenames:
            #----LOWER CASE TEST CASE----#
            test_file = os.path.join(self.temp_dir,
                                     test_filename['test'].lower())
            correct_file = os.path.join(self.temp_dir,
                                        test_filename['correct'].lower())
            with open(test_file, 'w'):
                pass
            videofile = self.video(test_file)
            videofile._Video__fix_season_episode_format()
            self.assertEqual(videofile.file, correct_file)
            os.remove(correct_file)

            #----UPPER CASE TEST CASE----#
            test_file = os.path.join(self.temp_dir,
                                     test_filename['test'].upper())
            correct_file = os.path.join(self.temp_dir,
                                        test_filename['correct'].upper())
            with open(test_file, 'w'):
                pass
            videofile = self.video(test_file)
            videofile._Video__fix_season_episode_format()
            self.assertEqual(videofile.file, correct_file)
            os.remove(correct_file)

    def test_fix_season_episode_format_numbers_only_one_episode(self):
        """Test conversion of SEE to sSSeEE
        """
        test_filenames = [
                           {
                             'test' : 'test.tv.101.resolution.mp4',
                             'correct' : 'test.tv.s01e01.resolution.mp4'
                           },
                           {
                             'test' : 'test.tv.1001.resolution.mp4',
                             'correct' : 'test.tv.s10e01.resolution.mp4'
                           },
                           {
                             'test' : 'test.tv.with.year.2018.101.resolution.mp4',
                             'correct' : 'test.tv.with.year.2018.s01e01.resolution.mp4'
                           }
                         ]

        for test_filename in test_filenames:
            #----LOWER CASE TEST CASE----#
            test_file = os.path.join(self.temp_dir,
                                     test_filename['test'].lower())
            correct_file = os.path.join(self.temp_dir,
                                        test_filename['correct'].lower())
            with open(test_file, 'w'):
                pass
            videofile = self.video(test_file)
            videofile._Video__fix_season_episode_format()
            self.assertEqual(videofile.file, correct_file)
            os.remove(correct_file)

    def test_fix_season_episode_format_numbers_only_two_episodes(self):
        """Test conversion of SEEEE to sSSeEEeEE
        """
        test_filenames = [
                           {
                             'test' : 'test.tv.10102.resolution.mp4',
                             'correct' : 'test.tv.s01e01e02.resolution.mp4'
                           },
                           {
                             'test' : 'test.tv.with.year.2018.10102.resolution.mp4',
                             'correct' : 'test.tv.with.year.2018.s01e01e02.resolution.mp4'
                           }
                         ]

        for test_filename in test_filenames:
            #----LOWER CASE TEST CASE----#
            test_file = os.path.join(self.temp_dir,
                                     test_filename['test'].lower())
            correct_file = os.path.join(self.temp_dir,
                                        test_filename['correct'].lower())
            with open(test_file, 'w'):
                pass
            videofile = self.video(test_file)
            videofile._Video__fix_season_episode_format()
            self.assertEqual(videofile.file, correct_file)
            os.remove(correct_file)

    def test_remove_proper_no_change(self):
        """Test to check that a file with no proper does not change
        """
        test_filenames = ["test.tv.s01e01.resolution.mp4"]
        for test_filename in test_filenames:
            #----LOWER CASE TEST CASE----#
            test_file = os.path.join(self.temp_dir, test_filename.lower())
            videofile = self.video(test_file)
            videofile.remove_proper()
            self.assertEqual(videofile.file, test_file)

            #----UPPER CASE TEST CASE----#
            test_file = os.path.join(self.temp_dir, test_filename.upper())
            videofile = self.video(test_file)
            videofile.remove_proper()
            self.assertEqual(videofile.file, test_file)

    def test_remove_proper_with_proper(self):
        """Test the removal of proper in filename
        """
        test_filenames = [
                           {
                             'test' : 'test.tv.s01e01.proper.resolution.mp4',
                             'correct' : 'test.tv.s01e01.resolution.mp4'
                           }
                         ]

        for test_filename in test_filenames:
            #----LOWER CASE TEST CASE----#
            test_file = os.path.join(self.temp_dir,
                                     test_filename['test'].lower())
            correct_file = os.path.join(self.temp_dir,
                                        test_filename['correct'].lower())
            with open(test_file, 'w'):
                pass
            videofile = self.video(test_file)
            videofile.remove_proper()
            self.assertEqual(videofile.file, correct_file)
            os.remove(correct_file)

            #----UPPER CASE TEST CASE----#
            test_file = os.path.join(self.temp_dir,
                                     test_filename['test'].upper())
            correct_file = os.path.join(self.temp_dir,
                                        test_filename['correct'].upper())
            with open(test_file, 'w'):
                pass
            videofile = self.video(test_file)
            videofile.remove_proper()
            self.assertEqual(videofile.file, correct_file)
            os.remove(correct_file)

    def test_remove_repack_no_change(self):
        """Test to check that a file with no repack does not change
        """
        test_filenames = ["test.tv.s01e01.resolution.mp4"]
        for test_filename in test_filenames:
            #----LOWER CASE TEST CASE----#
            test_file = os.path.join(self.temp_dir, test_filename.lower())
            videofile = self.video(test_file)
            videofile.remove_repack()
            self.assertEqual(videofile.file, test_file)

            #----UPPER CASE TEST CASE----#
            test_file = os.path.join(self.temp_dir, test_filename.upper())
            videofile = self.video(test_file)
            videofile.remove_repack()
            self.assertEqual(videofile.file, test_file)

    def test_remove_repack_with_repack(self):
        """Test the removal of repack in filename
        """
        test_filenames = [
                           {
                             'test' : 'test.tv.s01e01.repack.resolution.mp4',
                             'correct' : 'test.tv.s01e01.resolution.mp4'
                           }
                         ]

        for test_filename in test_filenames:
            #----LOWER CASE TEST CASE----#
            test_file = os.path.join(self.temp_dir,
                                     test_filename['test'].lower())
            correct_file = os.path.join(self.temp_dir,
                                        test_filename['correct'].lower())
            with open(test_file, 'w'):
                pass
            videofile = self.video(test_file)
            videofile.remove_repack()
            self.assertEqual(videofile.file, correct_file)
            os.remove(correct_file)

            #----UPPER CASE TEST CASE----#
            test_file = os.path.join(self.temp_dir,
                                     test_filename['test'].upper())
            correct_file = os.path.join(self.temp_dir,
                                        test_filename['correct'].upper())
            with open(test_file, 'w'):
                pass
            videofile = self.video(test_file)
            videofile.remove_repack()
            self.assertEqual(videofile.file, correct_file)
            os.remove(correct_file)

    def test_remove_internal_no_change(self):
        """Test to check that a file with no internal does not change
        """
        test_filenames = ["test.tv.s01e01.resolution.mp4"]
        for test_filename in test_filenames:
            #----LOWER CASE TEST CASE----#
            test_file = os.path.join(self.temp_dir, test_filename.lower())
            videofile = self.video(test_file)
            videofile.remove_internal()
            self.assertEqual(videofile.file, test_file)

            #----UPPER CASE TEST CASE----#
            test_file = os.path.join(self.temp_dir, test_filename.upper())
            videofile = self.video(test_file)
            videofile.remove_internal()
            self.assertEqual(videofile.file, test_file)

    def test_remove_internal_with_internal(self):
        """Test the removal of internal in filename
        """
        test_filenames = [
                           {
                             'test' : 'test.tv.s01e01.internal.resolution.mp4',
                             'correct' : 'test.tv.s01e01.resolution.mp4'
                           }
                         ]

        for test_filename in test_filenames:
            #----LOWER CASE TEST CASE----#
            test_file = os.path.join(self.temp_dir,
                                     test_filename['test'].lower())
            correct_file = os.path.join(self.temp_dir,
                                        test_filename['correct'].lower())
            with open(test_file, 'w'):
                pass
            videofile = self.video(test_file)
            videofile.remove_internal()
            self.assertEqual(videofile.file, correct_file)
            os.remove(correct_file)

            #----UPPER CASE TEST CASE----#
            test_file = os.path.join(self.temp_dir,
                                     test_filename['test'].upper())
            correct_file = os.path.join(self.temp_dir,
                                        test_filename['correct'].upper())
            with open(test_file, 'w'):
                pass
            videofile = self.video(test_file)
            videofile.remove_internal()
            self.assertEqual(videofile.file, correct_file)
            os.remove(correct_file)

    def test_move_to_movie(self):
        """Test the move to movie directory
        """
        test_filenames = [
                           {
                             'test' : 'test.movie.resolution.mp4',
                             'correct' : 'movie/test.movie.resolution.mp4'
                           }
                         ]

        for test_filename in test_filenames:
            #----LOWER CASE TEST CASE----#
            test_file = os.path.join(self.temp_dir,
                                     test_filename['test'].lower())
            correct_file = os.path.join(self.temp_dir,
                                        test_filename['correct'].lower())
            with open(test_file, 'w'):
                pass
            videofile = self.video(test_file)
            videofile.move_to_movie()
            self.assertEqual(videofile.file, correct_file)
            os.remove(correct_file)

    def test_move_to_tv(self):
        """Test the move to tv directory
        """
        test_filenames = [
                           {
                             'test' : 'test.tv.s01e01.resolution.mp4',
                             'correct' : 'tv/test.tv.s01e01.resolution.mp4'
                           }
                         ]

        for test_filename in test_filenames:
            #----LOWER CASE TEST CASE----#
            test_file = os.path.join(self.temp_dir,
                                     test_filename['test'].lower())
            correct_file = os.path.join(self.temp_dir,
                                        test_filename['correct'].lower())
            with open(test_file, 'w'):
                pass
            videofile = self.video(test_file)
            videofile.move_to_tv()
            self.assertEqual(videofile.file, correct_file)
            os.remove(correct_file)

    @unittest.skip('skipping because this function has side effects')
    def test_get_show_info_no_show(self):
        """Test getting show info when no show info is present
        """
        test_filenames = [
                           {
                             'test' : 'test.movie.resolution.mp4',
                             'correct' : (None, None, [])
                           }
                         ]

        for test_filename in test_filenames:
            #----LOWER CASE TEST CASE----#
            test_file = os.path.join(self.temp_dir,
                                     test_filename['test'].lower())
            videofile = self.video(test_file)
            show_info = videofile.get_show_info()
            self.assertEqual(show_info, test_filename["correct"])

    @unittest.skip('skipping because this function has side effects')
    def test_get_show_info_show(self):
        """Test getting show info when show info is present
        """
        test_filenames = [
                           {
                             'test' : 'test.tv.s01.e01.resolution.mp4',
                             'correct' : ("test.tv", "01", ["01"])
                           },
                           {
                             'test' : 'test.tv.s01.e01.e02.resolution.mp4',
                             'correct' : ("test.tv", "01", ["01", "02"])
                           }
                         ]

        for test_filename in test_filenames:
            #----LOWER CASE TEST CASE----#
            test_file = os.path.join(self.temp_dir,
                                     test_filename['test'].lower())
            with open(test_file, 'w'):
                pass
            videofile = self.video(test_file)
            show_info = videofile.get_show_info()
            self.assertEqual(show_info, test_filename["correct"])
            os.remove(test_file)

    @unittest.skip('skipping because this function has side effects')
    def test_get_show_info_show_not_real_show(self):
        """Test getting show info when show info is present but show is not real
        """
        test_filenames = [
                           {
                             'test' : 'test.tv.s01.e01.resolution.mp4',
                             'correct' : (None, None, [])
                           },
                           {
                             'test' : 'test.tv.s01.e01.e02.resolution.mp4',
                             'correct' : (None, None, [])
                           }
                         ]
        wareztools.scrapers.themoviedb.TheMovieDB.ret = False

        for test_filename in test_filenames:
            #----LOWER CASE TEST CASE----#
            test_file = os.path.join(self.temp_dir,
                                     test_filename['test'].lower())
            with open(test_file, 'w'):
                pass
            videofile = self.video(test_file)
            show_info = videofile.get_show_info()
            self.assertEqual(show_info, test_filename["correct"])
            os.remove(test_file)

    def test_all_functions(self):
        """Test all functions together
        """
        test_filenames = [
                             {
                               'test' : 'test.tv.with.year.2018.s01.e01.resolution.internal-GROUP.mp4',
                               'correct' : 'test.tv.with.year.2018.s01e01.resolution.mp4'
                             },
                             {
                               "test" : "test.tv.with.year.2018.s01.e01.resolution.repack-GROUP.mp4",
                               "correct" : "test.tv.with.year.2018.s01e01.resolution.mp4"
                             },
                             {
                               "test" : "test.tv.with.year.2018.s01.e01.resolution.proper-GROUP.mp4",
                               "correct" : "test.tv.with.year.2018.s01e01.resolution.mp4"
                             },
                             {
                               "test" : "test.tv.with.year.2018.s01.e01.e02.resolution.internal-GROUP.mp4",
                               "correct" : "test.tv.with.year.2018.s01e01e02.resolution.mp4"
                             },
                             {
                               "test" : "test.tv.with.year.2018.s01.e01.e02.resolution.repack-GROUP.mp4",
                               "correct" : "test.tv.with.year.2018.s01e01e02.resolution.mp4"
                             },
                             {
                               "test" : "test.tv.with.year.2018.s01.e01.e02.resolution.proper-GROUP.mp4",
                               "correct" : "test.tv.with.year.2018.s01e01e02.resolution.mp4"
                             },
                             {
                               "test" : "test.tv.with.year.2018.101.resolution.internal-GROUP.mp4",
                               "correct" : "test.tv.with.year.2018.s01e01.resolution.mp4"
                             },
                             {
                               "test" : "test.tv.with.year.2018.101.resolution.repack-GROUP.mp4",
                               "correct" : "test.tv.with.year.2018.s01e01.resolution.mp4"
                             },
                             {
                               "test" : "test.tv.with.year.2018.101.resolution.proper-GROUP.mp4",
                               "correct" : "test.tv.with.year.2018.s01e01.resolution.mp4"
                             },
                             {
                               "test" : "test.tv.with.year.2018.10102.resolution.internal-GROUP.mp4",
                               "correct" : "test.tv.with.year.2018.s01e01e02.resolution.mp4"
                             },
                             {
                               "test" : "test.tv.with.year.2018.10102.resolution.repack-GROUP.mp4",
                               "correct" : "test.tv.with.year.2018.s01e01e02.resolution.mp4"
                             },
                             {
                               "test" : "test.tv.with.year.2018.10102.resolution.proper-GROUP.mp4",
                               "correct" : "test.tv.with.year.2018.s01e01e02.resolution.mp4"
                             }
                         ]

        for test_filename in test_filenames:
            #----LOWER CASE TEST CASE----#
            test_file = os.path.join(self.temp_dir,
                                     test_filename['test'].lower())
            correct_file = os.path.join(self.temp_dir,
                                        test_filename['correct'].lower())
            with open(test_file, 'w'):
                pass
            videofile = self.video(test_file)
            videofile.remove_group()
            videofile.remove_internal()
            videofile.remove_proper()
            videofile.remove_repack()
            videofile._Video__fix_season_episode_format()
            self.assertEqual(videofile.file, correct_file)
            os.remove(correct_file)

if __name__ == "__main__":
    logging.basicConfig(format='%(module)s:%(funcName)s:%(lineno)d [%(levelname)s] %(message)s', level=logging.DEBUG)
    unittest.main()
