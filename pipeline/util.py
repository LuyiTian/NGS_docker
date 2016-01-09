## util.py
import datetime
import functools
import os
__TIME_FORMAT = "%Y-%m-%d %H:%M:%S"


def prep_dir(result_dir, sub_dir):
    """
    create sub folder, also create root folder if it does not exist
    """
    if not os.path.isdir(result_dir):
        os.mkdir(result_dir)
    sub_path = os.path.join(result_dir, sub_dir)
    if not os.path.isdir(sub_path):
        os.mkdir(sub_path)
    return sub_path


def run_task(tag_line):
    """
    a decorator to run command, add time tag and run info to output logs
    """
    def actualDecorator(func):
        @functools.wraps(func)
        def wrapper(obj, **kwargs):
            start_time = datetime.datetime.now().strftime(__TIME_FORMAT)
            obj.std_handle.write(tag_line.format(status="started", time=start_time, **kwargs))
            result = func(obj, **kwargs)
            end_time = datetime.datetime.now().strftime(__TIME_FORMAT)
            obj.std_handle.write(tag_line.format(status="ended", time=end_time, **kwargs))
            return result
        return wrapper

    return actualDecorator