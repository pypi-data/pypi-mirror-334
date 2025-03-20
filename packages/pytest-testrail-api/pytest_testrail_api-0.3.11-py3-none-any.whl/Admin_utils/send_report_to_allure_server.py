import os

from Admin_utils.allure_tools.allure_server_api_client import AllureServerClient
from App.config.driver_config import ALLURE_REPORT_PATH as APP_REPORT_PATH
from Rest.admin.config import ALLURE_REPORT_PATH as REST_REPORT_PATH
from Rest.admin.config import get_environ
from Web.config.driver import ALLURE_REPORT_PATH as WEB_REPORT_PATH

LANGUAGE = get_environ("LANGUAGE")
RUN_NAME = get_environ("RUN_NAME")
PLATFORM = get_environ("PLATFORM")
PROJECT_CONFIG = get_environ("PROJECT_CONFIG")
ALLURE_PATH = {"App": APP_REPORT_PATH, "Rest": REST_REPORT_PATH, "Web": WEB_REPORT_PATH}
ALLURE_PROJECT_ID = {
    "App_ipad": "app-ca-ipad",
    "App_iphone": "app-ca-iphone",
    "App_android_phone": "app-ca-android-phone",
    "App_android_tablet": "app-ca-android-tablet",
    "Rest": "rest",
    "Rest_videos": "rest-videos",
    "Web_en": "web-en",
    "Web_es": "web-es",
    "Web_chi": "web-chi",
    "Web_fr": "web-fr",
    "Web_de": "web-de",
}


def define_allure_folder_path():
    allure_folder_path = ""
    if "App" in PROJECT_CONFIG:
        allure_folder_path = os.path.join(
            f"{ALLURE_PATH[PROJECT_CONFIG]}/allure-results", f"{PLATFORM.lower()}"
        )
    elif "Rest" in PROJECT_CONFIG or "Web" in PROJECT_CONFIG:
        allure_folder_path = os.path.join(f"{ALLURE_PATH[PROJECT_CONFIG]}", "allure-results")
    return allure_folder_path


def define_allure_project_id():
    allure_id = ""
    if "App" in PROJECT_CONFIG:
        allure_id = ALLURE_PROJECT_ID[f"App_{PLATFORM.lower()}"]
    elif "Rest" in PROJECT_CONFIG:
        if "Videos" in RUN_NAME:
            allure_id = ALLURE_PROJECT_ID["Rest_videos"]
        else:
            allure_id = ALLURE_PROJECT_ID["Rest"]
    elif "Web" in PROJECT_CONFIG:
        allure_id = ALLURE_PROJECT_ID[f"Web_{LANGUAGE.lower()}"]
    return allure_id


if __name__ == "__main__":
    AllureServerClient.send_report_to_allure_server(
        allure_project_id=define_allure_project_id(), allure_folder=define_allure_folder_path()
    )
