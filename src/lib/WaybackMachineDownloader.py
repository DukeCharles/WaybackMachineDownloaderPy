import http.client

from src.lib import ArchiveAPI
import html
import re
import ssl

class WaybackMachineDownloader:
    def __init__(self, options):
        self.__options = options
        self.__base_url: str = options.get('base_url')
        self.__exact_url = options.get('exact_url')
        self.__directory = options.get('directory')
        self.__all_timestamps = options.get('all_timestamps')
        self.__from_timestamp = options.get('from_timestamp')
        self.__to_timestamp = options.get('to_timestamp')
        self.__only_filter = options.get('only_filter')
        self.__exclude_filter = options.get('exclude_filter')
        self.__all = options.get('all')
        # @__maximum_pages = params[:maximum_pages] ? params[:maximum_pages].to_i: 100
        # @__threads_count = params[:threads_count].to_i
        self.__maximum_pages = options.get('maximum_pages')
        self.__threads_count = options.get('threads_count')
    def backup_name(self):
        if "//" in self.__base_url:
            return self.__base_url.split('/')[2]
        else:
            return self.__base_url

    def backup_path(self):
        if self.__directory is not None:
            if self.__directory[-1] == '/':
                return self.__directory
            else:
                return self.__directory + '/'
        else:
            return 'websites/' + self.backup_name() + '/'

    def match_only_filter(self, file_url):
        if self.__only_filter:
            only_filter = re.compile(self.__only_filter)
            return bool(only_filter.search(file_url))
        else:
            return True

    def match_exclude_filter(self, file_url):
        if self.__exclude_filter:
            exclude_filter = re.compile(self.__exclude_filter)
            return bool(exclude_filter.search(file_url))
        else:
            return False

    def get_all_snapshots_to_consider(self):
        print("Getting snapshot pages. ", end='')
        snapshot_list_to_consider = []
        snapshot_list_to_consider += ArchiveAPI.get_raw_list_from_api(self.__base_url, self.__options)
        if self.__exact_url is None:
            for page_index in range(self.__maximum_pages):
                print("Page Index = "+str(page_index))
                params = {"page_index": page_index}
                snapshot_list = ArchiveAPI.get_raw_list_from_api(self.__base_url + "/*", params)
                if snapshot_list:
                    snapshot_list_to_consider += snapshot_list
        print(" found {snapshots_lst} snaphots to consider.".format(snapshots_lst=len(snapshot_list_to_consider)))
        return snapshot_list_to_consider

    def get_file_list_curated(self):
        file_list_curated = {}
        for snapshot in self.get_all_snapshots_to_consider():
            print(snapshot)  # TODO REMOVE AFTER
            file_timestamp = snapshot[0]
            file_url = snapshot[1]
            if "/" not in file_url:
                continue

            file_id = "/".join(file_url.split("/")[3:-1])
            file_id = html.unescape(file_id)

            if file_id != "":
                file_id = file_id  # TODO fix broken bytes in case

            if file_id is None:
                print('Malformed file url, ignoring: #{0}'.format(file_url))
            else:
                # If there is a exclude_filter
                if self.match_exclude_filter(file_url):
                    print('File url matches exclude filter, ignoring: #{0}'.format(file_url))
                elif not self.match_only_filter(file_url):
                    print("File url doesn't match only filter, ignoring: #{0}".format(file_url))
                elif file_list_curated[file_id]:
                    if not file_list_curated[file_id]["timestamp"] > file_timestamp:
                        file_list_curated[file_id] = {"file_url": file_url, "timestamp": file_timestamp}
                else:
                    file_list_curated[file_id] = {"file_url": file_url, "timestamp": file_timestamp}

        return file_list_curated

    def get_file_list_all_timestamps(self):
        file_list_curated = {}
        for snapshot in self.get_all_snapshots_to_consider():
            file_timestamp = snapshot[0]
            file_url = snapshot[1]
            if "/" not in file_url:
                continue

            file_id = "/".join(file_url.split("/")[3:-1])
            file_id_and_timestamp = '/'.join([file_timestamp, file_id])
            file_id_and_timestamp = html.unescape(file_id_and_timestamp)

            if file_id_and_timestamp != "":
                file_id_and_timestamp = file_id_and_timestamp  # TODO fix broken bytes in case

            if file_id is None:
                print('Malformed file url, ignoring: #{0}'.format(file_url))
            else:
                if self.match_exclude_filter(file_url):
                    print('File url matches exclude filter, ignoring: #{0}'.format(file_url))
                elif not self.match_only_filter(file_url):
                    print("File url doesn't match only filter, ignoring: #{0}".format(file_url))
                elif file_list_curated[file_id_and_timestamp]:
                    print("Duplicate file and timestamp combo, ignoring: #{0}".format(file_id))
                else:
                    file_list_curated[file_id_and_timestamp] = {"file_url": file_url, "timestamp": file_timestamp}

        print("file_list_curated: {0}".format(len(file_list_curated)))
        return file_list_curated

    def get_file_list_by_timestamp(self):
        if self.__all_timestamps:
            file_list_curated = self.get_file_list_all_timestamps()
            for file in file_list_curated:
                print(file)
        else:
            file_list_curated = self.get_file_list_curated()
            for file in file_list_curated:
                print(file)
        pass

    def list_files(self):
        files = self.get_file_list_by_timestamp()
        print(files)
        pass

    def download_files(self):
        pass

    def structure_dir_path(self, dir_path):
        pass

    def download_file(self, file_remote_info):
        pass

    def file_queue(self):
        pass

    def file_list_by_timestamp(self):
        pass

    def semaphore(self):
        pass
