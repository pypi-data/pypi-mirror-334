import os
import time


def file_not_old(file, age_seconds=5):
    try:
        if file_exists(file):
            file_age_mtime = _get_time(time.time()) - _get_time(file_age(file))
            if file_age_mtime > age_seconds:
                return False
            else:
                return True
        return False
    except Exception as e:
        print(f'caught {type(e)}: e')
        return False


def _get_time(float):
    return int(str(float).split('.', maxsplit=1)[0])


def file_exists(file_name):
    """Uses a filepath + filenam string and determines if the file exists"""
    if os.path.exists(file_name):
        return True
    return False


def file_age(file_path):
    """Returns the last modified unix time integer of a filepath + filename string"""
    file_to_open = file_path
    try:
        if file_exists(file_to_open):
            mtime = _get_time(os.path.getmtime(file_to_open))
            return mtime
    except Exception as e:
        print(f'caught {type(e)}: e')
        return False
