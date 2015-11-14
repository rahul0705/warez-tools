"""
author: Rahul Mohandas
"""
import unittest

from wareztools.scrapers.scraper import Scraper

class TestScraper(unittest.TestCase):
    """Test the Video class
    """

    def setUp(self):
        self.scraper = Scraper()

    def test_get_show_id(self):
        """Test to check that get_show_id is not implemented
        """
        self.assertRaises(NotImplementedError,
                          self.scraper.get_show_id,
                          "")

    def test_validate_show(self):
        """Test to check that validate_show is not implemented
        """
        self.assertRaises(NotImplementedError,
                          self.scraper.validate_show,
                          "")

    def test_validate_show_season(self):
        """Test to check that validate_show_season is not implemented
        """
        self.assertRaises(NotImplementedError,
                          self.scraper.validate_show_season,
                          "", "")

    def test_validate_show_episode(self):
        """Test to check that validate_show_episode is not implemented
        """
        self.assertRaises(NotImplementedError,
                          self.scraper.validate_show_episode,
                          "", "", "")

    def test_get_movie_id(self):
        """Test to check that get_movie_id is not implemented
        """
        self.assertRaises(NotImplementedError,
                          self.scraper.get_movie_id,
                          "")

    def test_validate_movie(self):
        """Test to check that validate_movie is not implemented
        """
        self.assertRaises(NotImplementedError,
                          self.scraper.validate_movie,
                          "")

if __name__ == "__main__":
    unittest.main()
