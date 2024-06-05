import unittest
import src.bin.CliArgumentsHandler as cli


class TestCliArgumentsHandler(unittest.TestCase):

    def setUp(self):
        self.parser = cli.parser

    def test_base_url_argument(self):
        args = self.parser.parse_args(['http://example.com'])
        self.assertEqual(args.base_url, 'http://example.com')

    def test_directory_argument(self):
        args = self.parser.parse_args(['http://example.com', '--directory',  '/path/to/dir'])
        self.assertEqual(args.directory, '/path/to/dir')

    def test_directory_alias_argument(self):
        args = self.parser.parse_args(['http://example.com', '-d', '/path/to/dir'])
        self.assertEqual(args.directory, '/path/to/dir')

    def test_all_timestamps_argument(self):
        args = self.parser.parse_args(['http://example.com', '--all-timestamps'])
        self.assertTrue(args.all_timestamps)

    def test_all_timestamps_alias_argument(self):
        args = self.parser.parse_args(['http://example.com', '-s'])
        self.assertTrue(args.all_timestamps)

    def test_from_argument(self):
        args = self.parser.parse_args(['http://example.com', '--from', '20060716231334'])
        self.assertEqual(args.from_timestamp, 20060716231334)

    def test_from_alias_argument(self):
        args = self.parser.parse_args(['http://example.com', '-f', '20060716231334'])
        self.assertEqual(args.from_timestamp, 20060716231334)

    def test_to_argument(self):
        args = self.parser.parse_args(['http://example.com', '--to', '20100916231334'])
        self.assertEqual(args.to_timestamp, 20100916231334)

    def test_to_alias_argument(self):
        args = self.parser.parse_args(['http://example.com', '-t', '20100916231334'])
        self.assertEqual(args.to_timestamp, 20100916231334)

    def test_exact_url_argument(self):
        args = self.parser.parse_args(['http://example.com', '--exact-url', 'http://example.com/page'])
        self.assertEqual(args.exact_url, 'http://example.com/page')

    def test_exact_url_alias_argument(self):
        args = self.parser.parse_args(['http://example.com', '-e', 'http://example.com/page'])
        self.assertEqual(args.exact_url, 'http://example.com/page')

    def test_only_argument(self):
        args = self.parser.parse_args(['http://example.com', '--only', 'filter'])
        self.assertEqual(args.only_filter, 'filter')

    def test_only_alias_argument(self):
        args = self.parser.parse_args(['http://example.com', '-o', 'filter'])
        self.assertEqual(args.only_filter, 'filter')

    def test_exclude_argument(self):
        args = self.parser.parse_args(['http://example.com', '--exclude', 'filter'])
        self.assertEqual(args.exclude_filter, 'filter')

    def test_exclude_alias_argument(self):
        args = self.parser.parse_args(['http://example.com', '-x', 'filter'])
        self.assertEqual(args.exclude_filter, 'filter')

    def test_all_argument(self):
        args = self.parser.parse_args(['http://example.com', '--all'])
        self.assertTrue(args.all)

    def test_all_alias_argument(self):
        args = self.parser.parse_args(['http://example.com', '-a'])
        self.assertTrue(args.all)

    def test_concurrency_argument(self):
        args = self.parser.parse_args(['http://example.com', '--concurrency', '5'])
        self.assertEqual(args.threads_count, 5)

    def test_concurrency_alias_argument(self):
        args = self.parser.parse_args(['http://example.com', '-c', '5'])
        self.assertEqual(args.threads_count, 5)

    def test_maximum_snapshot_argument(self):
        args = self.parser.parse_args(['http://example.com', '--maximum-snapshot', '200'])
        self.assertEqual(args.maximum_pages, '200')

    def test_maximum_snapshot_alias_argument(self):
        args = self.parser.parse_args(['http://example.com', '-p', '200'])
        self.assertEqual(args.maximum_pages, '200')

    def test_list_argument(self):
        args = self.parser.parse_args(['http://example.com', '--list'])
        self.assertTrue(args.list)

    def test_list_alias_argument(self):
        args = self.parser.parse_args(['http://example.com', '-l'])
        self.assertTrue(args.list)

    def test_version_argument(self):
        with self.assertRaises(SystemExit) as cm:
            self.parser.parse_args(['--version'])
        self.assertEqual(cm.exception.code, 0)

    def test_version_alias_argument(self):
        with self.assertRaises(SystemExit) as cm:
            self.parser.parse_args(['-v'])
        self.assertEqual(cm.exception.code, 0)


if __name__ == '__main__':
    unittest.main()