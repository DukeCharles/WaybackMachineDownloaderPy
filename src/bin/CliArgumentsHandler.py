import argparse
from src.lib.WaybackMachineDownloader import WaybackMachineDownloader

parser = argparse.ArgumentParser(prog='WaybackMachineDownloader',
                    description='Download an entire website from the Wayback Machine.',
                    epilog='Text at the bottom of help')

parser.add_argument('base_url', help='You need to specify a website to backup. (e.g., http://example.com)\nRun `wayback_machine_downloader --help` for more help.')

parser.add_argument('-d', '--directory', action='store', dest='directory', metavar='PATH', help='Directory to save the downloaded files into\nDefault is ./websites/ plus the domain name')

parser.add_argument('-s', '--all-timestamps', action='store_true', dest='all_timestamps', help='Download all snapshots/timestamps for a given website')

parser.add_argument('-f', '--from',  action='store', type=int, dest='from_timestamp', metavar='TIMESTAMP', help='Only files on or after timestamp supplied (ie. 20060716231334)')

parser.add_argument('-t', '--to', action='store', type=int, dest='to_timestamp', metavar='TIMESTAMP', help='Only files on or before timestamp supplied (ie. 20100916231334)')

parser.add_argument('-e', '--exact-url', action='store', dest='exact_url', metavar='URL', help='Download only the url provided and not the full site')

parser.add_argument('-o', '--only', action='store', dest='only_filter', metavar='ONLY_FILTER', help='Restrict downloading to urls that match this filter\n(use // notation for the filter to be treated as a regex)')

parser.add_argument('-x', '--exclude', action='store', dest='exclude_filter', metavar='EXCLUDE_FILTER', help='Skip downloading of urls that match this filter\n(use // notation for the filter to be treated as a regex)')

parser.add_argument('-a', '--all', action='store_true', dest='all', help='Expand downloading to error files (40x and 50x) and redirections (30x)')

parser.add_argument('-c', '--concurrency', action='store', type=int, dest='threads_count', metavar='NUMBER', help='Expand downloading to error files (40x and 50x) and redirections (30x)', default=1)

parser.add_argument('-p', '--maximum-snapshot', action='store', dest='maximum_pages', metavar='NUMBER', help='Maximum snapshot pages to consider (Default is 100)\nCount an average of 150,000 snapshots per page', default=100)

parser.add_argument('-l', '--list', action='store_true', dest='list', help='Only list file urls in a JSON format with the archived timestamps, won\'t download anything')

parser.add_argument('-v', '--version', action='version', version='%(prog)s 2.0')


args = parser.parse_args()

wayback_machine_downloader = WaybackMachineDownloader(vars(args))

if args.list:
    print("Print list")
    wayback_machine_downloader.list_files()
else:
    print("Download site")
    wayback_machine_downloader.download_files()


