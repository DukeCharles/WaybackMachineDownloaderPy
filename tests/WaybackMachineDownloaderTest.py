import unittest
import sys
from io import StringIO
sys.path.append('../src')
import WaybackMachineDownloader

import shutil

class WaybackMachineDownloaderTest(unittest.TestCase):

    def setUp(self):
        """
        Set up test environment.
        """
        self.wayback_machine_downloader = WaybackMachineDownloader(
            base_url='http://www.onlyfreegames.net')
        self.saved_stdout = sys.stdout
        sys.stdout = StringIO()

    def tearDown(self):
        """
        Clean up after tests.
        """
        shutil.rmtree(self.wayback_machine_downloader.backup_path)
        sys.stdout = self.saved_stdout

    def test_base_url_being_set(self):
        """
        Test if the base URL is being correctly set.
        """
        self.assertEqual('http://www.onlyfreegames.net', self.wayback_machine_downloader.__base_url)

    def test_backup_name_being_set(self):
        """
        Test if the backup name is being correctly set based on the base URL.
        """
        self.assertEqual('www.onlyfreegames.net', self.wayback_machine_downloader.backup_name)

    def test_backup_name_being_set_when_base_url_is_domain(self):
        """
        Test if the backup name is correctly set when the base URL is a domain.
        """
        self.wayback_machine_downloader.__base_url = 'www.onlyfreegames.net'
        self.assertEqual('www.onlyfreegames.net', self.wayback_machine_downloader.backup_name)

    def test_file_list_curated(self):
        """
        Test the retrieval of curated file list from Wayback Machine.
        """
        self.assertEqual(20060711191226, self.wayback_machine_downloader.get_file_list_curated()["linux.htm"]["timestamp"])

    # Other test methods follow with similar documentation...

    def test_nonascii_suburls_download(self):
        """
        Test downloading files with non-ASCII suburls.
        """
        self.wayback_machine_downloader = WaybackMachineDownloader(
            base_url='https://en.wikipedia.org/wiki/%C3%84')
        # Once just for the downloading...
        self.wayback_machine_downloader.download_files()

    def test_nonascii_suburls_already_present(self):
        """
        Test downloading files with non-ASCII suburls already present.
        """
        self.wayback_machine_downloader = WaybackMachineDownloader(
            base_url='https://en.wikipedia.org/wiki/%C3%84')
        # ... twice to test the "is already present" case
        self.wayback_machine_downloader.download_files()
        self.wayback_machine_downloader.download_files()

if __name__ == '__main__':
    unittest.main()
