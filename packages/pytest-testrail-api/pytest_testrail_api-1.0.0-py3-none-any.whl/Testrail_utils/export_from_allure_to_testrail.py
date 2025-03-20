import ast
import glob
import json
import os
from time import sleep


def get_cases_from_testrail(client, run_id):
    return client.tests.get_tests(run_id=run_id)


def get_cases_from_allure(allure_folder_path):
    os.popen(f"allure generate {allure_folder_path} --clean -o {allure_folder_path}/report")
    sleep(10)
    all_cases_from_allure = []
    for file in glob.glob(os.path.join(f"{allure_folder_path}/report/data/test-cases", "*.json")):
        with open(file, encoding="utf-8", mode="r") as test_case:
            test_case_dict = dict(json.load(test_case))
            # Get case name from allure and transform it to TR format
            if len(test_case_dict["parameters"]):
                parameters = ast.literal_eval(test_case_dict["parameters"][0]["value"])
                case_name = test_case_dict["name"]
                # replace parameters in allure test name string
                for key, value in parameters.items():
                    key = f"<{key}>"
                    case_name = case_name.replace(key, value)
                # remove square brackets from end of the test name string
                parameters_in_case_name = "[" + case_name.split("[")[-1]
                case_name = case_name.replace(parameters_in_case_name, "")
            else:
                case_name = test_case_dict["name"]
            # when test marked with bug number allure print it in test name and it should be removed
            if "BUG" in case_name:
                case_name = case_name.split(":")[1]
            # cut off empty spaces on both sides
            case_name = case_name.strip()
            case_status = test_case_dict["status"]
            all_cases_from_allure.append({"case_name": case_name, "result": case_status})
    return all_cases_from_allure


def filter_cases_and_set_testrail_case_id_for_allure_cases(all_cases_from_allure, all_cases_from_testrail):
    for case in all_cases_from_allure:
        case["case_id"] = next(
            (tr_case.case_id for tr_case in all_cases_from_testrail if tr_case.title == case["case_name"]), None
        )
    #   remove cases that have no TR id but present in allure report
    invalid_cases = [case for case in all_cases_from_allure if case["case_id"] is None]
    print(f"Case is not in run or have invalid name {invalid_cases}")
    return [case for case in all_cases_from_allure if case["case_id"] is not None]


def prepare_result_data(all_cases_from_allure, add_only_passed_test, testrail_case_statuses):
    if add_only_passed_test:
        case_results = [case for case in all_cases_from_allure if case["result"] == "passed"]
        for case in case_results:
            case["status_id"] = testrail_case_statuses["passed"]
            case.pop("case_name")
            case.pop("result")
    else:
        case_results = [
            case for case in all_cases_from_allure if case["result"] == "passed" or case["result"] == "failed"
        ]
        for case in case_results:
            if case["result"] == "passed":
                case["status_id"] = testrail_case_statuses["passed"]
            else:
                case["status_id"] = testrail_case_statuses["failed"]
            case.pop("case_name")
            case.pop("result")
    return case_results
