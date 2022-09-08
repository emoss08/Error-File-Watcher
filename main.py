from os import listdir
import os
from os.path import isfile, join
import time

watch_directory = r'errorfile/'
file_name = 'error'
pollTime = 5


class FileWatcherError(Exception):
    """ Custom exception for file watcher """
    pass


def file_in_directory(my_dir: str) -> list[str]:
    """ Returns a list of files in a directory """
    only_files: list[str] = [f for f in listdir(my_dir) if isfile(join(my_dir, f))]
    return only_files


def list_comparison(original_list: list, new_list: list) -> list:
    """ Returns a list of items in NewList that are not in OriginalList """
    differences_list = [x for x in new_list if
                        x not in original_list]
    return differences_list


def error_file_present(new_files: list):
    """ Do something with the new files """
    if new_files == ['error']:
        print('Error file has been created')
        try:
            os.remove(watch_directory + file_name)
            print('Error file has been removed')
        except FileWatcherError as file_watcher_error:
            print(file_watcher_error)
            exit(1)


def file_watcher(my_dir: str, poll_time: int):
    """ Watches a directory for new files """
    while True:
        if 'watching' not in locals():
            previous_file_list: list[str] = file_in_directory(watch_directory)
            watching = 1
            print('Watching ....')

        time.sleep(pollTime)

        new_file_list: list[str] = file_in_directory(watch_directory)

        file_diff: list = list_comparison(previous_file_list, new_file_list)

        previous_file_list = new_file_list
        if len(file_diff) == 0:
            continue
        error_file_present(file_diff)


file_watcher(watch_directory, pollTime)
