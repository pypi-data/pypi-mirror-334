import os
from datetime import datetime

from cmdline_preparse_hook.allure_report_path import CURRENT_DIRECTORY

env_file = "C:\\Users\\Yevhen\\PycharmProjects\\demoqa_com\\allure-results\\chrome\\environment.properties"

folder_path = CURRENT_DIRECTORY + "\\allure-results\\chrome"


def get_env():
    today = datetime.now()
    time_now = today.strftime("%Y/%m/%d %H:%M:%S")
    with open(folder_path + "\\environment.properties", "w") as file:
        file.write("OS_platform = linux" "\nOS_browser = Chrome" f"\ndate = {time_now}")


if __name__ == "__main__":
    get_env()
    os.popen('allure serve "C:\\Users\\Yevhen\\PycharmProjects\\demoqa_com\\allure-results\\chrome"')
