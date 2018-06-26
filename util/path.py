from pathlib import Path
import os


def string_after_last_slash(to_cut):
    cut_list = to_cut.split('/')
    if len(cut_list) == 0:
        return ''
    else:
        return cut_list[-1]


def compare_filenames_in_path(first, second):
    name_first = string_after_last_slash(first)
    name_second = string_after_last_slash(second)
    return name_first == name_second


def path_points_to_file(path):
    pathlib_path = Path(path)
    return pathlib_path.exists() and pathlib_path.is_file()


def path_points_to_directory(path):
    pathlib_path = Path(path)
    return pathlib_path.exists() and pathlib_path.is_dir()


def create_directory(path):
    pathlib_path = Path(path)
    pathlib_path.mkdir(parents=True, exist_ok=True)


def get_files_in_dir(path, end_with=None):
    files = []
    if end_with:
        for file in os.listdir(path):
            if file.endswith(end_with):
                files.append(file)
    else:
        for file in os.listdir(path):
            files.append(file)
    return files
