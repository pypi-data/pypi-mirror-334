import ast
import datetime
import email.mime.application
import glob
import json
import logging
import os
import shutil
import sys
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import boto3
from botocore.exceptions import BotoCoreError, ClientError

from Admin_utils.custom_logger import logger
from Admin_utils.get_time_from_drone.calculate_total_runtime import delete_json_file, get_final_run_time
from Admin_utils.get_time_from_drone.time_logger import json_path
from Admin_utils.helper_constant_data.helper_constants import tr_icon_image
from App.config.driver_config import ALLURE_REPORT_PATH as APP_REPORT_PATH
from Rest.admin.config import ALLURE_REPORT_PATH as REST_REPORT_PATH
from Rest.admin.config import get_environ
from Testrail_utils.config import TR_PROJECT_ID
from Testrail_utils.pytest_testrail_api_client.test_rail import TestRail
from Web.config.driver import ALLURE_REPORT_PATH as WEB_REPORT_PATH

PROJECT_CONFIG = get_environ("PROJECT_CONFIG")
RUN_NAME = get_environ("RUN_NAME")
PLATFORM = get_environ("PLATFORM")
PLATFORM_AND_APP = get_environ("PLATFORM_AND_APP")
MAIL_ADDRESS = get_environ("MAIL_ADDRESS")
MAIL_PASSWORD = get_environ("MAIL_PASSWORD")
MAIL_ADDRESS_OAUTH = get_environ("MAIL_ADDRESS_OAUTH")
MAIL_PASSWORD_OAUTH = get_environ("MAIL_PASSWORD_OAUTH")
ENVIRONMENT = get_environ("ENVIRONMENT")
LANGUAGE = get_environ("LANGUAGE")
ALLURE_PATH = {"App": APP_REPORT_PATH, "Rest": REST_REPORT_PATH, "Web": WEB_REPORT_PATH}
CREATE_ALLURE_REPORT = get_environ("CREATE_ALLURE_REPORT")
TEST_MODE = get_environ("TEST_MODE")
SEND_MAIL = get_environ("SEND_MAIL")

ALLURE_CATEGORIES = [
    {"name": "Ignored tests", "matchedStatuses": ["skipped"]},
    {"name": "Infrastructure problems", "matchedStatuses": ["broken", "failed"], "messageRegex": ".*bye-bye.*"},
    {"name": "Outdated tests", "matchedStatuses": ["broken"], "traceRegex": ".*FileNotFoundException.*"},
    {"name": "Failed tests", "matchedStatuses": ["failed"]},
    {
        "name": "Broken tests without correspond TR case",
        "matchedStatuses": ["broken"],
        "messageRegex": ".*Cases without correspond tests in TR.*",
    },
]

logging.basicConfig(level=logging.DEBUG)


class Archive:
    def __init__(self, folder_path):
        self.passed = self.failed = self.total = 0
        self.folder_path = folder_path
        file_name = os.path.join(os.path.dirname(folder_path), "tmp_zip")
        self.zip_file_name = f"{file_name}.zip"
        if os.path.isfile(self.zip_file_name):
            os.remove(self.zip_file_name)
        for file in (
            result for result in os.listdir(folder_path) if result.split(".")[-1] not in ("json", "properties")
        ):
            os.remove(os.path.join(folder_path, file))

        shutil.make_archive(base_name=file_name, root_dir=folder_path, format="zip")
        self.json_files = [
            os.path.join(folder_path, file)
            for file in os.listdir(folder_path)
            if file.endswith(".json") and "categories" not in file
        ]

    def get_statistic(self):
        names = set()
        for file in self.json_files:
            with open(file, "r") as f:
                data = json.load(f)
                if data.get("name") not in names:
                    status = data.get("status")
                    if status == "passed":
                        self.passed += 1
                    elif status in ["failed", "unknown"]:
                        self.failed += 1
                    names.add(data["name"])

        self.total = self.passed + self.failed

    def send_mail(self, delete_archive: bool = False):
        self.get_statistic()
        addr_from = MAIL_ADDRESS
        get_time = get_final_run_time()

        addr_to = (
            ["email_for@test.com"]
            if TEST_MODE
            else ["3d4m-qa-allure-report-aaaaeqo6443rn7cxhycrmjjz3m@elsevier.org.slack.com"]
        )
        run_name = RUN_NAME or ""
        extension = self.zip_file_name.split(".")[-1]
        main_name = (
            f'{PROJECT_CONFIG} {run_name} {PLATFORM} tests results on {datetime.datetime.today().strftime("%d.%m.%Y")}'
        )

        with open(self.zip_file_name, "rb") as file:
            file_to_send = email.mime.application.MIMEApplication(file.read())
            file_to_send.add_header("Content-Disposition", "attachment", filename=f"{main_name}.{extension}")

        body = self._compose_body(get_time)
        logger.info(f"body: {body}")

        ses_client = boto3.client("ses", region_name="us-east-2")

        msg = MIMEMultipart()
        msg["From"] = addr_from
        msg["To"] = ", ".join(addr_to)
        msg["Subject"] = main_name

        msg.attach(MIMEText(body, "plain"))
        msg.attach(file_to_send)

        try:
            response = ses_client.send_raw_email(
                Source=addr_from,
                Destinations=addr_to,
                RawMessage={"Data": msg.as_string()},
            )
            logging.info(f"Email sent! Message ID: {response['MessageId']}")
        except (BotoCoreError, ClientError) as error:
            logging.error(f"Failed to send email: {error}")

        if delete_archive:
            os.remove(self.zip_file_name)
            delete_json_file(json_path)

    def _compose_body(self, get_time):
        if "App" in PROJECT_CONFIG:
            return f"{PLATFORM}, executed {self.total} tests\nTotal passed - {self.passed}\nTotal failed - {self.failed}\nTotal time - {get_time}"
        elif PROJECT_CONFIG in ["Web", "Grasshopper"]:
            return f"Executed on {LANGUAGE}, {ENVIRONMENT} - {self.total} tests\nTotal passed - {self.passed}\nTotal failed - {self.failed}"
        elif "Rest" in PROJECT_CONFIG:
            body = f"Executed {self.total} tests\nTotal passed - {self.passed}\nTotal failed - {self.failed}"
            if "-m" in sys.argv:
                body += f'\n\nMarks: {sys.argv[sys.argv.index("-m") + 1]}'
            return body


def get_cases_names_from_allure(report_path):
    list_of_cases_names = []
    for file in glob.glob(os.path.join(report_path, "*.json")):
        with open(file, encoding="utf-8", mode="r") as test_case:
            test_case_dict = json.load(test_case)
            case_name = test_case_dict["name"]
            if "parameters" in test_case_dict:
                parameters = ast.literal_eval(test_case_dict["parameters"][0]["value"])
                for key, value in parameters.items():
                    case_name = case_name.replace(f"<{key}>", value)
                case_name = case_name.split("[")[0].strip()
            if "BUG" in case_name:
                case_name = case_name.split(":")[1].strip()
            list_of_cases_names.append({"tr_case_name": case_name, "original_allure_case_name": test_case_dict["name"]})
    return list_of_cases_names


def set_tr_links_for_allure_cases(list_of_cases_names, tr_cases, report_path):
    for case in list_of_cases_names:
        case["case_id"] = next(
            (tr_case.id for tr_case in tr_cases if tr_case.title == case["tr_case_name"]),
            "Case name is not found in TR base, please review",
        )

    unique_cases = [dict(case_tuple) for case_tuple in {tuple(case.items()) for case in list_of_cases_names}]

    for file in glob.glob(os.path.join(report_path, "*.json")):
        with open(file, encoding="utf-8", mode="r") as test_case:
            test_case_dict = json.load(test_case)

        for case in unique_cases:
            if test_case_dict["name"] == case["original_allure_case_name"]:
                link = (
                    ""
                    if "not found" in str(case["case_id"])
                    else f"https://3d4medical.testrail.net/index.php?/cases/view/{str(case['case_id'])}"
                )
                link_text = case["case_id"] if "not found" in str(case["case_id"]) else "Link to TR case"
                link_style = "color:red;" if "not found" in str(case["case_id"]) else ""
                final_link = f"<a style='{link_style}' href ='{link}' target='_blank'>{link_text}</a>"
                tr_icon = f'<img style="display: inline-block;vertical-align: middle;" width="40px" height="40px" src="data:image/svg+xml;base64,{tr_icon_image}">'
                description_html = test_case_dict.get("descriptionHtml", "")
                test_case_dict["descriptionHtml"] = f"{description_html}<br>{final_link}{tr_icon}"

                if "not found" in str(case["case_id"]):
                    test_case_dict["statusDetails"] = (
                        {"message": "Cases without correspond tests in TR"}
                        if test_case_dict["status"] == "passed"
                        else {
                            "message": f"{test_case_dict['statusDetails']['message']} Cases without correspond tests in TR"
                        }
                    )
                    test_case_dict["status"] = "broken"

        with open(file, encoding="utf-8", mode="w") as test_case:
            json.dump(test_case_dict, test_case)


def prepare_allure_results(report_path):
    tr_cases = TestRail().cases.get_cases(project_id=20, suite_id=TR_PROJECT_ID[PROJECT_CONFIG])
    list_of_cases_names = get_cases_names_from_allure(report_path)
    set_tr_links_for_allure_cases(list_of_cases_names, tr_cases, report_path)


def send_mail():
    if CREATE_ALLURE_REPORT and SEND_MAIL:
        report_path = (
            os.path.join(f"{ALLURE_PATH[PROJECT_CONFIG]}/allure-results", f"{PLATFORM.lower()}")
            if PROJECT_CONFIG == "App"
            else os.path.join(f"{ALLURE_PATH[PROJECT_CONFIG]}", "allure-results")
        )
        prepare_allure_results(report_path)
        if PROJECT_CONFIG == "App":
            env_variables = {"PLATFORM": PLATFORM, "PLATFORM_AND_APP": PLATFORM_AND_APP}
            with open(f"{report_path}/environment.properties", "w") as env_file:
                env_file.write("\n".join(f"{key}={value}" for key, value in env_variables.items()))

        with open(f"{report_path}/categories.json", "w") as allure_categories:
            json.dump(ALLURE_CATEGORIES, allure_categories)
        Archive(report_path).send_mail(delete_archive=True)
        print("Report sent")


if __name__ == "__main__":
    send_mail()
