import glob
import json
import os
import shutil

from Testrail_utils.pytest_testrail_api_client.test_rail import TestRail

RUN_ID = os.environ.get("RUN_ID", "")
PLATFORM_AND_APP = os.environ.get("PLATFORM_AND_APP", "")
PLATFORM = os.environ.get("PLATFORM", "")
PROJECT_CONFIG = os.environ.get("PROJECT_CONFIG", "")
EXPORT_RESULT_IN_TESTRAIL = os.environ.get("EXPORT_RESULT_IN_TESTRAIL", "")

path_to_rep = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SESSION_RESULT_PATH = {
    "App": f"{path_to_rep}/App/config/results",
    "Rest": f"{path_to_rep}/Rest/admin/results",
    "Web": f"{path_to_rep}/Web/config/results",
    "Grasshopper": f"{path_to_rep}/Grasshopper/config/results",
    "SDK-Web": f"{path_to_rep}/SDK/Web/config/results",
}

TESTRAIL_CASE_STATUSES = {"passed": 1, "failed": 5}


def get_tests_from_session(project):
    all_cases_from_run = []
    result_path = ""
    if project == "App":
        result_path = f"{SESSION_RESULT_PATH[project]}/{PLATFORM.lower()}"
    else:
        result_path = f"{SESSION_RESULT_PATH[project]}"

    for file in glob.glob(os.path.join(result_path, "*.json")):
        with open(file, encoding="utf-8", mode="r") as test_case:
            test_case_dict = json.load(test_case)
            case_name = test_case_dict["case_name"]
            case_parameters = test_case_dict.get("params")
            if case_parameters:
                for key, value in case_parameters.items():
                    key = f"<{key}>"
                    case_name = case_name.replace(key, value)
            all_cases_from_run.append(
                {
                    "case_name": case_name,
                    "result": test_case_dict["result"],
                    "steps": test_case_dict["steps"],
                    "error_log": test_case_dict["error_log"],
                }
            )
    return all_cases_from_run


def prepare_steps_result(cases):
    for case in cases:
        steps = []
        for step in case["steps"]:
            step_result = "passed" if not step["failed"] else "failed"
            data = {
                "content": f"**{step['keyword']}:**{step['name']}",
                "status_id": TESTRAIL_CASE_STATUSES[step_result],
                "actual": case["error_log"] if step_result == "failed" else "",
            }
            steps.append(data)
            if step_result == "failed":
                break
        case["custom_step_results"] = steps


def filter_cases_and_set_testrail_case_id(all_cases_from_run, cases_from_tr_run):
    for case in all_cases_from_run:
        case["case_id"] = next(
            (tr_case.case_id for tr_case in cases_from_tr_run if tr_case.title == case["case_name"]), None
        )

    return [case for case in all_cases_from_run if case["case_id"] is not None]


def prepare_result_in_tr_format(all_cases_from_run):
    case_results = [case for case in all_cases_from_run if case["result"] in TESTRAIL_CASE_STATUSES]
    for case in case_results:
        case_result = case["result"]
        case["status_id"] = TESTRAIL_CASE_STATUSES[case_result]
        case.pop("case_name")
        case.pop("result")
    return case_results


def export_result(project, delete_session_result_dir):
    tr_client = TestRail()
    cases_from_tr_run = tr_client.tests.get_tests(run_id=RUN_ID)
    all_cases_from_run = get_tests_from_session(project)
    filtered_cases = filter_cases_and_set_testrail_case_id(
        all_cases_from_run=all_cases_from_run, cases_from_tr_run=cases_from_tr_run
    )
    prepare_steps_result(filtered_cases)
    result_data = prepare_result_in_tr_format(filtered_cases)
    tr_client.results.add_results_for_cases(run_id=int(RUN_ID), results=result_data)
    if delete_session_result_dir:
        shutil.rmtree(SESSION_RESULT_PATH[PROJECT_CONFIG])


if __name__ == "__main__":
    export_result(project=PROJECT_CONFIG, delete_session_result_dir=True)
    print("Export completed")
