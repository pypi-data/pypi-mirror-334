from Testrail_utils.copy_test_result_from_one_run_to_another import export_results
from Testrail_utils.create_run import get_config, get_id_test_run, get_run_info, setup_test_run
from Testrail_utils.export_from_allure_to_testrail import (
    filter_cases_and_set_testrail_case_id_for_allure_cases,
    get_cases_from_allure,
    get_cases_from_testrail,
    prepare_result_data,
)
from Testrail_utils.export_to_exel import export_old_regression_test_cases_to_exel
from Testrail_utils.pytest_testrail_api_client.test_rail import TestRail

ALLURE_FOLDER_PATH = ""  # folder name e.g. App_IPAD
MILESTONE_NAME = ""  # 11.1.0
TEST_PLANE_NAME = ""  # 'CA'25 | 11.1.0 RoW Regression'
TEST_SUITE_NAME = ""  # device = ["iPad", "iPhone", "Android Tablet", "Android Phone"]
ADD_ONLY_PASSED_TEST = True
TESTRAIL_CASE_STATUSES = {"passed": 1, "failed": 5}


def get_run_id_in_test_plan(plan_name: str, name_run: str) -> int:
    plans_api = TestRail()
    project_id = 20
    plan_id = plans_api.runs.get_plan_id_by_name(project_id, plan_name)
    if plan_id is None:
        print(f"\033[91mTest Plan '{plan_name}' not found\033[0m")
        return None
    else:
        info_test_plan = plans_api.runs.get_plan_info(plan_id)
        id_regression_run = None
        name_run.replace("(", "").replace(")", "")
        if len(info_test_plan.entries[0].runs) > 1:
            for config in range(len(info_test_plan.entries[0].runs)):
                if str(info_test_plan.entries[0].runs[config]) in name_run:
                    id_regression_run = info_test_plan.entries[0].runs[config].id
                    url = info_test_plan.entries[0].runs[config].url
                    print(
                        "\033[38;5;200m" + f"ID {TEST_SUITE_NAME} Regression test run: " + "\033[0m", id_regression_run
                    )
                    print("\033[38;5;200m" + f"Link {TEST_SUITE_NAME} Regression test run: " + "\033[0m", url)
                    break
        else:
            for config in range(len(info_test_plan.entries)):
                if str(info_test_plan.entries[config].runs[0]) in name_run:
                    id_regression_run = info_test_plan.entries[config].runs[0].id
                    url = info_test_plan.entries[config].runs[0].url
                    print(
                        "\033[38;5;200m" + f"ID {TEST_SUITE_NAME} Regression test run: " + "\033[0m", id_regression_run
                    )
                    print("\033[38;5;200m" + f"Link {TEST_SUITE_NAME} Regression test run: " + "\033[0m", url)
                    break
        if id_regression_run is None:
            print(f"\033[91mTest Run '{name_run}' not found in Plan '{plan_name}'\033[0m")
            return None
        else:
            return id_regression_run


def create_auto_run(milestone_name):
    if "(" in TEST_SUITE_NAME and ")" in TEST_SUITE_NAME:
        device_name = TEST_SUITE_NAME.replace("(", "").replace(")", "").split("App ")[1]
    else:
        device_name = TEST_SUITE_NAME
    regression, ui_type, device, version = get_config(device=device_name, version=milestone_name)
    run_name = f"{device} auto run {version}"
    if setup_test_run(run_name, regression, ui_type):
        run_id = get_id_test_run(run_name)
        run_info = get_run_info(run_id)
        print(f"Auto Run ID: {run_id}")
        print(f"Link {TEST_SUITE_NAME} Auto Run in TestRail: ", run_info.url)
        return run_id
    else:
        run_id = get_id_test_run(run_name)
        run_info = get_run_info(run_id)
        print(f"Auto Run ID: {run_id}")
        print(f"Link {TEST_SUITE_NAME} Auto Run in TestRail: ", run_info.url)
        exit()


def export_from_allure(run_id):
    test_rail = TestRail()
    get_cases_with_tr_id_and_result = filter_cases_and_set_testrail_case_id_for_allure_cases(
        get_cases_from_allure(ALLURE_FOLDER_PATH), get_cases_from_testrail(test_rail, run_id)
    )
    results = prepare_result_data(get_cases_with_tr_id_and_result, ADD_ONLY_PASSED_TEST, TESTRAIL_CASE_STATUSES)
    test_rail.results.add_results_for_cases(run_id=run_id, results=results)


def copy_results_to_regression_run(auto_run_id, test_plane_name, test_suite_name):
    REGRESSION_RUN_ID = get_run_id_in_test_plan(test_plane_name, test_suite_name)
    export_results(old_run_id=auto_run_id, new_run_id=REGRESSION_RUN_ID)
    export_old_regression_test_cases_to_exel(auto_run_id)


if __name__ == "__main__":
    AUTO_RUN_ID = create_auto_run(MILESTONE_NAME)
    export_from_allure(AUTO_RUN_ID)
    copy_results_to_regression_run(AUTO_RUN_ID, TEST_PLANE_NAME, TEST_SUITE_NAME)
