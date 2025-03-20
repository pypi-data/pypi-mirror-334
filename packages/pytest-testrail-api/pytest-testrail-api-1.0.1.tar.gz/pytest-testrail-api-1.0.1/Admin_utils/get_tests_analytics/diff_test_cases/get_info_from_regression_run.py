import json
import os

from Testrail_utils.pytest_testrail_api_client.test_rail import TestRail

GET_INFO_FROM_RUN_PATH = os.environ.get("GET_INFO_FROM_RUN_PATH", os.path.dirname(__file__))
duration = int(os.environ.get("DURATION", 0))

test_rail = TestRail()
automation_status = {"draft": 6, "to_automate": 1, "automated": 4, "manual": 5, "suite": None}
type = {"archive": 1, "rare": 15, "regression": 9, "critical": 13, "smoke": 11}

automation_tag = "manual"
type_tag = "archive"
RUN_ID = 1672
json_data = {}
json_path = os.path.join(GET_INFO_FROM_RUN_PATH, f"{RUN_ID}.json")


def get_cases_from_testrail(client, automation_tag, type_tag):
    tests = client.tests.get_tests(run_id=RUN_ID)
    all_tests_from_run = [test.id for test in tests]
    tests_automation_type = [
        test.id for test in tests if test.custom_automation_type == automation_status[automation_tag]
    ]
    tests_type = [test.id for test in tests if test.type_id == type[type_tag]]
    json_data["All tests in Test Rail run"] = f"{len(all_tests_from_run)}: {all_tests_from_run}"
    json_data[f"{automation_tag} tests in Test Rail run"] = f"{len(tests_automation_type)}: {tests_automation_type}"
    json_data[f"{type_tag} tests in Test Rail run"] = f"{len(tests_type)}: {tests_type}"


def get_info_for_all_tags():
    tag = 0
    automation_tag = []
    type_tag = []
    [automation_tag.append(tag_auto) for tag_auto, number in automation_status.items()]
    [type_tag.append(tag_type) for tag_type, number in type.items()]
    for _ in range(4):
        get_cases_from_testrail(test_rail, automation_tag[tag], type_tag[tag])
        tag += 1


def add_info_to_json():
    data = json.load(open(json_path))
    data.append(json_data)
    with open(json_path, "w") as file:
        json.dump(data, file, indent=2)


def create_json(json_path):
    json_data = []
    if not os.path.exists(json_path):
        with open(json_path, "w") as file:
            file.write(json.dumps(json_data))
        add_info_to_json()
    else:
        add_info_to_json()


# The results will be written to a json file in the diff_test_cases folder
if __name__ == "__main__":
    get_info_for_all_tags()
    create_json(json_path)
