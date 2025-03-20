import os
import re
from typing import Dict, List, Tuple, Union

from Admin_utils.custom_logger import logger
from Testrail_utils.config import PROJECT_DIRECTORY
from Testrail_utils.pytest_testrail_api_client.service import get_feature
from Testrail_utils.pytest_testrail_api_client.test_rail import TestRail

# Constants
DEFAULT_PROJECT_NAME = "Sdk"
PROJECT_ID = 20

PROJECT_CONFIG = os.environ.get("PROJECT_CONFIG", PROJECT_DIRECTORY.keys())


def get_feature_paths(project_path: str) -> List[str]:
    paths_list = []
    for root, dirs, files in os.walk(project_path):
        for file in files:
            if file.endswith(".feature"):
                paths_list.append(os.path.join(root, file))
    return paths_list


def find_tag_line_number(path: str, tag: str) -> int:
    with open(path, "r") as file:
        for line_number, line in enumerate(file, 1):
            if tag in line:
                return line_number
    return -1


def format_path_to_file(path: str, line_number: int) -> str:
    return 'File "%s", line %d' % (path, line_number)


def get_all_cases(project_config: Union[str, List[str]] = PROJECT_CONFIG) -> Dict[int, Tuple[str, int]]:
    """
    The get_all_cases function retrieves all test cases from feature files for specified projects.
    """
    test_rail = TestRail()  # The function initializes a TestRail client to interact with the TestRail API.
    if isinstance(project_config, str):
        project_config = [project_config]

    all_cases = {}
    for project in project_config:  # The function iterates over each project in the project_config list.
        project_cases = {}
        # For each project, the function retrieves the paths of all .feature files in the project's directory
        # using the get_feature_paths function.
        paths_list = get_feature_paths(PROJECT_DIRECTORY[project])
        for path in paths_list:
            # For each feature file, the function attempts to retrieve the feature data using the get_feature function.
            # If an error occurs, it logs the error and continues to the next file.
            try:
                feature = get_feature(path, test_rail)
            except Exception:
                logger.error(f"Verify invalid feature file - {path}")
                continue

            for scenario in feature.children:
                # For each scenario in the feature file, the function extracts the tags and identifies
                # TestRail scenario IDs using a regular expression.
                tags_dicts = scenario["scenario"]["tags"]
                all_scenario_tags = [tag["name"] for tag in tags_dicts]

                tr_scenarios_ids = re.findall(r"@C(\d+)", str(all_scenario_tags))
                if tr_scenarios_ids:
                    # If TestRail scenario IDs are found, the function stores the scenario data,
                    # including the path to the case and the tags, in a dictionary.
                    for tr_id in tr_scenarios_ids:
                        line_number = find_tag_line_number(path, f"@C{tr_id}")
                        case_id = int(tr_id)
                        path_to_case = format_path_to_file(path, line_number)
                        project_cases[case_id] = {
                            "path_to_case": path_to_case,
                            "tags": all_scenario_tags,
                        }
                        logger.debug(f"🔖 Case ID: {case_id} {path_to_case}")
        # The function logs the number of tests and unique tests found in the feature files for each project.
        logger.info(f"{project}: 🚀 Number of tests in project in feature files: {len(project_cases)}")
        logger.info(
            f"{project}: 🚀 Number of unique tests in project in feature files: {len(set(project_cases.keys()))}"
        )
        all_cases.update(project_cases)

    # The function returns a dictionary containing all the test cases for the specified projects.
    return all_cases


if __name__ == "__main__":
    ...
