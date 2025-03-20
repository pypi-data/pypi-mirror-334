import glob
import json
import os
import random
import shutil
import string
import subprocess
from time import sleep


def remove_obj_from_dict(list, label_name):
    for obj in list:
        if label_name in obj["name"]:
            list.remove(obj)


def run_allure_instance_with_all_report_from_dir(reports_dir):
    reports_dirs = os.listdir(reports_dir)
    reports_dirs = [dir for dir in reports_dirs if ".DS_Store" not in dir]
    for report in reports_dirs:
        for file in glob.glob(os.path.join(f"{reports_dir}/{report}", "*.json")):
            with open(file, encoding="utf-8", mode="r+") as test_case_result:
                test_case_dict = json.load(test_case_result)
                remove_obj_from_dict(test_case_dict["labels"], "parentSuite")
                remove_obj_from_dict(test_case_dict["labels"], "epic")
                test_case_dict[
                    "uuid"
                ] = f"{''.join(random.choices(string.ascii_letters, k=8))}-{''.join(random.choices(string.ascii_letters, k=4))}-{''.join(random.choices(string.ascii_letters, k=4))}-{''.join(random.choices(string.ascii_letters, k=4))}-{''.join(random.choices(string.ascii_letters, k=12))}"
                test_case_dict["historyId"] = f"{''.join(random.choices(string.ascii_letters, k=32))}"
                test_case_dict["labels"].append({"name": "parentSuite", "value": f"{report}"})
                test_case_dict["labels"].append({"name": "epic", "value": f"{report}"})
                test_case_result.seek(0)
                test_case_result.write(json.dumps(test_case_dict))
                test_case_result.truncate()
        files = os.listdir(f"{reports_dir}/{report}")
        for file in files:
            os.makedirs(f"{reports_dir}/temp", exist_ok=True)
            shutil.copy(f"{reports_dir}/{report}/{file}", f"{reports_dir}/temp")
    subprocess.Popen(["allure", "serve", f"{reports_dir}/temp"])
    sleep(10)
    shutil.rmtree(f"{reports_dir}/temp")


if __name__ == "__main__":
    run_allure_instance_with_all_report_from_dir(reports_dir="")
