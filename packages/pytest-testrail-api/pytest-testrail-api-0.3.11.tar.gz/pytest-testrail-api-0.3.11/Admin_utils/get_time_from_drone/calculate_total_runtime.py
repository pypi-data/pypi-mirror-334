import json
import os

from Admin_utils.get_time_from_drone.time_logger import json_path


def get_all_test_runtimes():
    get_all_time = 0
    with open(json_path) as file:
        data = json.load(file)
        for elem in data:
            for time in elem.values():
                get_all_time += int(time)
    return get_all_time


def seconds_to_hms(seconds):
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    return hours, minutes, seconds


def delete_json_file(json_path):
    if os.path.exists(json_path):
        os.remove(json_path)


def get_final_run_time():
    hours, minutes, seconds = seconds_to_hms(get_all_test_runtimes())
    return f"{int(hours)} hours, {int(minutes)} minutes, {int(seconds)} seconds"


get_final_run_time()
