import os
import re

from setuptools.namespaces import flatten

from Testrail_utils.config import PROJECT_DIRECTORY, TR_PROJECT_ID
from Testrail_utils.pytest_testrail_api_client.service import get_feature
from Testrail_utils.pytest_testrail_api_client.test_rail import TestRail

PROJECT_CONFIG = os.environ.get("PROJECT_CONFIG", "App")


def get_feature_paths(project_path):
    paths_list = []
    for root, dirs, files in os.walk(project_path):
        for file in files:
            if file.endswith(".feature"):
                paths_list.append(os.path.join(root, file))
    return paths_list


def create_run(required_tags, at_least_one_tag_should_be, run_name, ui_type=None, platform=None):
    test_rail = TestRail()
    paths_list = get_feature_paths(PROJECT_DIRECTORY[PROJECT_CONFIG])
    print(paths_list)
    all_ids = []
    for path in paths_list:
        try:
            feature = get_feature(path, test_rail)
        except Exception:
            print(f"Verify invalid feature file - {path}")
        for scenario in feature.children:
            tags_dicts = scenario["scenario"]["tags"]
            all_scenario_tags = [tag["name"] for tag in tags_dicts]

            check_platform = platform is not None
            check_ui_type = ui_type is not None
            is_scenario_matched = False

            if all(tag in all_scenario_tags for tag in required_tags) and any(
                tag in all_scenario_tags for tag in at_least_one_tag_should_be
            ):
                is_scenario_matched = True
                if check_platform:
                    if any(tag in all_scenario_tags for tag in platform):
                        pass
                    else:
                        is_scenario_matched = False
                if check_ui_type:
                    if any(tag in all_scenario_tags for tag in ui_type):
                        pass
                    else:
                        is_scenario_matched = False
            if is_scenario_matched:
                for tag in all_scenario_tags:
                    ids = re.findall("@C(\d+)", tag)
                    all_ids.append(ids)

    all_ids = list(flatten(all_ids))
    all_ids = [int(id) for id in all_ids]
    print(all_ids)
    print("Number of tests: ", len(all_ids))
    invalid_ids = get_tests_with_invalid_ids(all_ids)
    if len(invalid_ids) == 0:
        # create run
        test_rail.runs.add_run(
            suite_id=TR_PROJECT_ID[PROJECT_CONFIG], name=run_name, case_ids=all_ids, include_all=False
        )
        print("\033[94mRun created\033[0m")
    else:
        print("\033[93minvalid tests ids:\033[0m")
        print(invalid_ids)
        print("\033[91mRun wasn't created\033[0m")
        exit()


def get_tests_with_invalid_ids(all_ids):
    test_rail = TestRail()
    tests = test_rail.cases.get_cases(project_id=20, suite_id=70)
    tests_ids_from_tr = [test.id for test in tests]
    invalid_ids = [id for id in all_ids if id not in tests_ids_from_tr]
    return invalid_ids


def delete_run(run_id):
    test_rail = TestRail()
    test_rail.runs.delete_run(run_id=run_id)


def get_run_info(run_id):
    test_rail = TestRail()
    run = test_rail.runs.get_run(run_id)
    return run


def get_config(device, version):
    if device in ["iPad", "iPhone"]:
        regression = "@regression"
    else:
        regression = "@android_adapted"
    if device in ["iPad", "Android Tablet"]:
        ui_type = "@tablet"
    else:
        ui_type = "@phone"
    return regression, ui_type, device, version


def setup_test_run(run_name, regression, ui_type):
    check_test_run = get_id_test_run(run_name)
    if check_test_run is not None:
        print("\033[93mRun already exist\033[0m")
        print("\033[91mNew run wasn't created\033[0m")
        return False
    else:
        create_run(
            required_tags=["@automated"],
            at_least_one_tag_should_be=[
                "@suite1",
                "@suite2",
                "@suite3",
                "@suite4",
                "@suite5",
                f"{regression}",
                "@critical",
                "@smoke",
            ],
            ui_type=["@all_ui", f"{ui_type}"],
            run_name=run_name,
        )
        return True


def get_id_test_run(name: str) -> int:
    test_rail = TestRail()
    project_id = 20
    run_id = test_rail.runs.get_run_id_by_name(project_id, name)
    return run_id

    # exemple of setup run
    # create_run(specific_tags=['@automated'], tags_should_be_included_in_run=['@purchases', '@videos'], run_name='Rest daily')
