import unittest
import os
import errno
import shutil
import tempfile
from wareztools.file import WarezFile

class TestWarezFile(unittest.TestCase):

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

    def testRemoveGroup(self):
        #Test to make sure if there is no group the filename does not change
        test_filename_without_group = "test.file.name.with.no.group.txt"
        wf = WarezFile(os.path.join(self.temp_dir, test_filename_without_group))
        wf.remove_group()
        self.assertEqual(os.path.basename(wf.filename),
                         test_filename_without_group,
                         msg="Filename changed")

        #Test to make sure if there is a group it will remove it
        test_filename_with_group = "test.file.name.with.group-GROUPNAME.txt"
        test_filename_without_group = "test.file.name.with.group.txt"
        wf = WarezFile(os.path.join(self.temp_dir, test_filename_with_group))
        wf.remove_group()
        self.assertEqual(os.path.basename(wf.filename),
                         test_filename_without_group,
                         msg="Group was not removed")

        #Test to make sure if there is a group with underscore it will remove it
        test_filename_with_group = "test.file.name.with.group-GROUP_NAME.txt"
        test_filename_without_group = "test.file.name.with.group.txt"
        wf = WarezFile(os.path.join(self.temp_dir, test_filename_with_group))
        wf.remove_group()
        self.assertEqual(os.path.basename(wf.filename),
                         test_filename_without_group,
                         msg="Group was not removed")

    def testFixShow(self):
        #Test correctly formatted file
        test_filename_sXXeXX = "test.tv.show.s01e01.resolution.txt"
        wf = WarezFile(os.path.join(self.temp_dir,
                                    test_filename_sXXeXX))
        wf.fix_show()
        self.assertEqual(os.path.basename(wf.filename), test_filename_sXXeXX,
                         msg="Filename changed")

        #Test for extra dot
        test_filename_sXXdoteXX = "test.tv.show.s01.e01.resolution.txt"
        test_filename_sXXeXX = "test.tv.show.s01e01.resolution.txt"
        wf = WarezFile(os.path.join(self.temp_dir,
                                    test_filename_sXXdoteXX))
        wf.fix_show()
        self.assertEqual(os.path.basename(wf.filename), test_filename_sXXeXX,
                         msg="sXX.eXX was not converted to sXXeXX")

        #Test for 3 digit number
        test_filename_XXX = "test.tv.show.101.resolution.txt"
        test_filename_sXXeXX = "test.tv.show.s01e01.resolution.txt"
        wf = WarezFile(os.path.join(self.temp_dir, test_filename_XXX))
        wf.fix_show()
        self.assertEqual(os.path.basename(wf.filename), test_filename_sXXeXX,
                         msg="XXX was not converted to sXXeXX")

        #Test correctly formatted file
        test_filename_sXXeXXeXX = "test.tv.show.s01e01e02.resolution.txt"
        wf = WarezFile(os.path.join(self.temp_dir, test_filename_sXXeXXeXX))
        wf.fix_show()
        self.assertEqual(os.path.basename(wf.filename),
                         test_filename_sXXeXXeXX,
                         msg="Filename changed")

        #Test for extra dot
        test_filename_sXXdoteXXdoteXX = ("test.tv.show.s01."
                                        "e01.e02.resolution.txt")
        test_filename_sXXeXXeXX = "test.tv.show.s01e01e02.resolution.txt"
        wf = WarezFile(os.path.join(self.temp_dir,
                                    test_filename_sXXdoteXXdoteXX))
        wf.fix_show()
        self.assertEqual(os.path.basename(wf.filename),
                         test_filename_sXXeXXeXX,
                         msg="sXX.eXX.eXX was not converted to sXXeXXeXX")

        #Test for 5 digit number
        test_filename_XXXXX = "test.tv.show.10102.resolution.txt"
        test_filename_sXXeXXeXX = "test.tv.show.s01e01e02.resolution.txt"
        wf = WarezFile(os.path.join(self.temp_dir, test_filename_XXXXX))
        wf.fix_show()
        self.assertEqual(os.path.basename(wf.filename),
                         test_filename_sXXeXXeXX,
                         msg="XXXXX was not converted to sXXeXXeXX")

        #Test Movie
        test_filename_movie = "test.movie.2015.resolution.txt"
        wf = WarezFile(os.path.join(self.temp_dir, test_filename_movie))
        wf.fix_show()
        self.assertEqual(os.path.basename(wf.filename),
                         test_filename_movie,
                         msg="Movie file changed")

if __name__ == "__main__":
    unittest.main()
