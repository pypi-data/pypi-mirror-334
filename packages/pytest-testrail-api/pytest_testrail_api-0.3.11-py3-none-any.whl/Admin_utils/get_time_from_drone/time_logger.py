import json
import os

PATH_FOR_DRONE_METHODS = os.environ.get("PATH_FOR_DRONE_METHODS", os.path.dirname(__file__))
json_path = os.path.join(PATH_FOR_DRONE_METHODS, "run_time.json")
duration = int(os.environ.get("DURATION", 0))


def add_time_to_json(time):
    json_data = {"Run_time": time}
    data = json.load(open(json_path))
    data.append(json_data)
    with open(json_path, "w") as file:
        json.dump(data, file, indent=2)


def create_json(json_path):
    json_data = []
    if not os.path.exists(json_path):
        with open(json_path, "w") as file:
            file.write(json.dumps(json_data))
        add_time_to_json(duration)
    else:
        add_time_to_json(duration)
    print(f"Duration: {duration} seconds")


create_json(json_path)
