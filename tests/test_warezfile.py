"""
author: Rahul Mohandas
"""
import unittest
import os
import errno
import shutil
import tempfile
import logging
import sys

import wareztools.warezfile

class TestWarezFile(unittest.TestCase):
    """Test the Video class
    """

    def setUp(self):
        # Create short hand for warezfile module
        self.warezfile = wareztools.warezfile.WarezFile
        try:
            # Create two temp dirs so we can test changing dirs
            self.temp_dir1 = tempfile.mkdtemp()
            self.temp_dir2 = tempfile.mkdtemp()
        except:
            try:
                # If we fail at making any temp dir clean yourself up
                shutil.rmtree(self.temp_dir1)
                shutil.rmtree(self.temp_dir2)
            except OSError as exc:
                if exc.errno != errno.ENOENT:
                    raise

    def tearDown(self):
        try:
            # Clean temp dirs up
            shutil.rmtree(self.temp_dir1)
            shutil.rmtree(self.temp_dir2)
        except OSError as exc:
            if exc.errno != errno.ENOENT:
                raise

    def test_file_abs_path(self):
        """Test file property gets created correctly with abs path
        """
        test_filenames = ['test.file.name.mp4']

        for test_filename in test_filenames:
            #----LOWER CASE TEST CASE----#
            test_file = os.path.join(self.temp_dir1, test_filename.lower())
            warezfile = self.warezfile(test_file)
            self.assertEqual(warezfile.file, test_file)

            #----UPPER CASE TEST CASE----#
            test_file = os.path.join(self.temp_dir1, test_filename.upper())
            warezfile = self.warezfile(test_file)
            self.assertEqual(warezfile.file, test_file)

    def test_file_no_path(self):
        """Test file property gets created correctly with no path
        """
        test_filenames = ['test.file.name.mp4']

        os.chdir(self.temp_dir1)
        for test_filename in test_filenames:
            #----LOWER CASE TEST CASE----#
            test_file = test_filename.lower()
            warezfile = self.warezfile(test_file)
            self.assertEqual(warezfile.file, test_file)

            #----UPPER CASE TEST CASE----#
            test_file = test_filename.upper()
            warezfile = self.warezfile(test_file)
            self.assertEqual(warezfile.file, test_file)

    def test_rename_filename_abs_path(self):
        """Test changing the filename property moves the file with abs path
        """
        test_filenames = [
                           {
                             'test' : 'test.file.name.mp4',
                             'correct' : 'test.file.name.2.mp4'
                           }
                         ]

        for test_filename in test_filenames:
            #----LOWER CASE TEST CASE----#
            original_test_file = os.path.join(self.temp_dir1,
                                              test_filename['test'].lower())
            new_test_file = os.path.join(self.temp_dir1,
                                         test_filename['correct'].lower())
            with open(original_test_file, 'w'):
                pass
            warezfile = self.warezfile(original_test_file)
            warezfile.filename = os.path.splitext(test_filename['correct'])[0]
            self.assertEqual(warezfile.file, new_test_file)
            self.assertTrue(os.path.isfile(new_test_file))
            self.assertFalse(os.path.isfile(original_test_file))
            os.remove(new_test_file)

            #----UPPER CASE TEST CASE----#
            original_test_file = os.path.join(self.temp_dir1,
                                              test_filename['test'].lower())
            new_test_file = os.path.join(self.temp_dir1,
                                         test_filename['correct'].lower())
            with open(original_test_file, 'w'):
                pass
            warezfile = self.warezfile(original_test_file)
            warezfile.filename = os.path.splitext(test_filename['correct'])[0]
            self.assertEqual(warezfile.file, new_test_file)
            self.assertTrue(os.path.isfile(new_test_file))
            self.assertFalse(os.path.isfile(original_test_file))
            os.remove(new_test_file)

    def test_rename_filename_no_path(self):
        """Test changing the filename property moves the file with no path
        """
        test_filenames = [
                           {
                             'test' : 'test.file.name.mp4',
                             'correct' : 'test.file.name.2.mp4'
                           }
                         ]

        os.chdir(self.temp_dir1)
        for test_filename in test_filenames:
            #----LOWER CASE TEST CASE----#
            original_test_file = test_filename['test'].lower()
            new_test_file = test_filename['correct'].lower()
            with open(original_test_file, 'w'):
                pass
            warezfile = self.warezfile(original_test_file)
            warezfile.filename = os.path.splitext(test_filename['correct'])[0]
            self.assertEqual(warezfile.file, new_test_file)
            self.assertTrue(os.path.isfile(new_test_file))
            self.assertFalse(os.path.isfile(original_test_file))
            os.remove(new_test_file)

            #----UPPER CASE TEST CASE----#
            original_test_file = test_filename['test'].lower()
            new_test_file = test_filename['correct'].lower()
            with open(original_test_file, 'w'):
                pass
            warezfile = self.warezfile(original_test_file)
            warezfile.filename = os.path.splitext(test_filename['correct'])[0]
            self.assertEqual(warezfile.file, new_test_file)
            self.assertTrue(os.path.isfile(new_test_file))
            self.assertFalse(os.path.isfile(original_test_file))
            os.remove(new_test_file)

    def test_rename_path_abs_path(self):
        """Test changing the path property moves the file with abs path
        """
        test_filenames = ['test.file.name.mp4']

        for test_filename in test_filenames:
            #----LOWER CASE TEST CASE----#
            original_test_file = os.path.join(self.temp_dir1,
                                              test_filename.lower())
            new_test_file = os.path.join(self.temp_dir2,
                                         test_filename.lower())
            with open(original_test_file, 'w'):
                pass
            warezfile = self.warezfile(original_test_file)
            warezfile.path = self.temp_dir2
            self.assertEqual(warezfile.file, new_test_file)
            self.assertTrue(os.path.isfile(new_test_file))
            self.assertFalse(os.path.isfile(original_test_file))
            os.remove(new_test_file)

            #----UPPER CASE TEST CASE----#
            original_test_file = os.path.join(self.temp_dir1,
                                              test_filename.lower())
            new_test_file = os.path.join(self.temp_dir2,
                                         test_filename.lower())
            with open(original_test_file, 'w'):
                pass
            warezfile = self.warezfile(original_test_file)
            warezfile.path = self.temp_dir2
            self.assertEqual(warezfile.file, new_test_file)
            self.assertTrue(os.path.isfile(new_test_file))
            self.assertFalse(os.path.isfile(original_test_file))
            os.remove(new_test_file)

    def test_rename_path_no_path(self):
        """Test changing the path property moves the file with no path
        """
        test_filenames = ['test.file.name.mp4']

        os.chdir(self.temp_dir1)
        for test_filename in test_filenames:
            #----LOWER CASE TEST CASE----#
            original_test_file = test_filename.lower()
            new_test_file = os.path.join(self.temp_dir2,
                                         test_filename.lower())
            with open(original_test_file, 'w'):
                pass
            warezfile = self.warezfile(original_test_file)
            warezfile.path = self.temp_dir2
            self.assertEqual(warezfile.file, new_test_file)
            self.assertTrue(os.path.isfile(new_test_file))
            self.assertFalse(os.path.isfile(original_test_file))
            os.remove(new_test_file)

            #----UPPER CASE TEST CASE----#
            original_test_file = test_filename.upper()
            new_test_file = os.path.join(self.temp_dir2,
                                         test_filename.upper())
            with open(original_test_file, 'w'):
                pass
            warezfile = self.warezfile(original_test_file)
            warezfile.path = self.temp_dir2
            self.assertEqual(warezfile.file, new_test_file)
            self.assertTrue(os.path.isfile(new_test_file))
            self.assertFalse(os.path.isfile(original_test_file))
            os.remove(new_test_file)

    def test_group_with_no_group(self):
        """Test group property when no group present in file
        """
        test_filenames = ['test.file.name.mp4']

        for test_filename in test_filenames:
            #----LOWER CASE TEST CASE----#
            test_file = os.path.join(self.temp_dir1,
                                     test_filename.lower())
            warezfile = self.warezfile(test_file)
            self.assertEquals(warezfile.scene_group, '')

            #----UPPER CASE TEST CASE----#
            test_file = os.path.join(self.temp_dir1,
                                     test_filename.upper())
            warezfile = self.warezfile(test_file)
            self.assertEquals(warezfile.scene_group, '')

    def test_group_with_group(self):
        """Test group property when group present in file
        """
        test_filenames = [
                           {
                             'file' : 'test.file.name-awesome_group.mp4',
                             'group' : 'awesome_group'
                           }
                         ]

        for test_filename in test_filenames:
            #----LOWER CASE TEST CASE----#
            test_file = os.path.join(self.temp_dir1,
                                     test_filename['file'].lower())
            warezfile = self.warezfile(test_file)
            self.assertEquals(warezfile.scene_group,
                              test_filename['group'].lower())

            #----UPPER CASE TEST CASE----#
            test_file = os.path.join(self.temp_dir1,
                                     test_filename['file'].upper())
            warezfile = self.warezfile(test_file)
            self.assertEquals(warezfile.scene_group,
                              test_filename['group'].upper())

if __name__ == '__main__':
    logging.basicConfig(format='%(module)s:%(funcName)s:%(lineno)d [%(levelname)s] %(message)s', level=logging.DEBUG)
    unittest.main()
