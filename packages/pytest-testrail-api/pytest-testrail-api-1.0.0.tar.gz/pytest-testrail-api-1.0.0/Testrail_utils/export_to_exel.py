import os

import xlsxwriter

from App.config.driver_config import PATH_TO_OLD_REGRESSION_TESTS
from Testrail_utils.pytest_testrail_api_client.api.service_api import TEST_CASES_ISNT_INCLUDED_IN_NEW_RUN
from Testrail_utils.pytest_testrail_api_client.test_rail import TestRail


def table_creation(run_id):
    folder_path = os.path.join(PATH_TO_OLD_REGRESSION_TESTS, "old_regression_tests")
    os.makedirs(folder_path, exist_ok=True)
    name_file = f"{TestRail().runs.get_run(run_id)}" + ".xlsx"
    table_path = os.path.join(folder_path, name_file)
    workbook = xlsxwriter.Workbook(table_path)
    worksheet = workbook.add_worksheet()
    return workbook, worksheet


def get_test_cases(set_test_cases):
    data = {"ID": [], "Name": [], "Link": []}
    for test_case in set_test_cases:
        data_row = test_case.split(" ", 1)
        if len(data_row) > 1:
            data["ID"].append(data_row[0])
            data["Name"].append(data_row[1])
            data["Link"].append(f"https://3d4medical.testrail.net/index.php?/tests/view/{data_row[0]}")
        else:
            print(f"Test case {data_row[0]} doesn't exist")

    return data


def export_old_regression_test_cases_to_exel(run_id):
    workbook, worksheet = table_creation(run_id)
    test_case_data = get_test_cases(TEST_CASES_ISNT_INCLUDED_IN_NEW_RUN)
    header_format = workbook.add_format({"bold": True, "underline": True, "align": "center"})
    for col_num, header in enumerate(test_case_data.keys()):
        worksheet.write(0, col_num, header, header_format)

    url_format = workbook.add_format({"color": "blue", "underline": True})
    for row_num, (id, name, link) in enumerate(
        zip(test_case_data["ID"], test_case_data["Name"], test_case_data["Link"]), 1
    ):
        worksheet.write(row_num, 0, id)
        worksheet.write_url(row_num, 2, link, url_format, string="Link to TestRail")
        worksheet.write(row_num, 1, name)

    workbook.close()
