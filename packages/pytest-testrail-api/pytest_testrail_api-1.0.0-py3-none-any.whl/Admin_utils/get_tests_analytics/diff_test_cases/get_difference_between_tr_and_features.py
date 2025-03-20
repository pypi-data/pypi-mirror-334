from typing import Dict

from Admin_utils.custom_logger import logger
from Admin_utils.get_tests_analytics.diff_test_cases.get_all_ids_cases_from_features import get_all_cases
from Testrail_utils.config import TESTRAIL_PATH_TO_CASE, TR_PROJECT_ID
from Testrail_utils.pytest_testrail_api_client.test_rail import TestRail

# Constants
DEFAULT_PROJECT_NAME = "App"
PROJECT_ID = 20


def get_all_cases_from_tr(project: str = DEFAULT_PROJECT_NAME, tr_session=None) -> Dict[int, str]:
    test_rail = tr_session or TestRail()
    tests_from_tr = test_rail.cases.get_cases(project_id=PROJECT_ID, suite_id=TR_PROJECT_ID[project])
    tr_tests_ids = {test.id: f"{TESTRAIL_PATH_TO_CASE}/{test.id}" for test in tests_from_tr}

    logger.info(f"{project}: 🚀 Number of tests in project in TrstRail: {len(tr_tests_ids)}")

    return tr_tests_ids


def log_inconsistant_scenarios_information(inconsistant_scenarios, issue_location: str = None):
    inconcistancies_number = len(inconsistant_scenarios)
    if inconcistancies_number:
        logger.warning(f"❌ There are {inconcistancies_number} inconsistant scenarios which are not in {issue_location}")
        for id, path in inconsistant_scenarios.items():
            logger.warning(f"🔖 {id} - {path}")
    else:
        logger.info(f"✅ All tests are in {issue_location}")


def get_tests_with_invalid_ids(
    project: str = DEFAULT_PROJECT_NAME, feature_test_ids=None, tr_tests_ids=None
) -> Dict[str, int]:
    feature_test_ids = feature_test_ids or get_all_cases(project)
    tr_tests_ids = tr_tests_ids or get_all_cases_from_tr(project)

    invalid_ids_from_auto_project = {id: feature_test_ids[id] for id in feature_test_ids if id not in tr_tests_ids}
    invalid_ids_from_tr = {id: tr_tests_ids[id] for id in tr_tests_ids if id not in feature_test_ids}

    logger.info(f"\033[1;94mProject: {project}\033[0m")

    not_corresponding_ids_dict = {
        "Project": project,
        "feature_test_number": len(feature_test_ids),
        "tr_tests_number": len(tr_tests_ids),
        "test_not_in_tr": invalid_ids_from_auto_project,
        "test_not_in_features": invalid_ids_from_tr,
    }

    return not_corresponding_ids_dict


if __name__ == "__main__":
    """
    Check if there are tests that aren't in Test Rail or in feature files.
    All inconsistencies will be logged in debug mode.
    All inconsistencies should be resolved before merging to the main branch.
    """
    check_results = get_tests_with_invalid_ids("App")
    assert not check_results[
        "test_not_in_tr"
    ], f"There are tests that aren't in Test Rail: {check_results['test_not_in_tr']}"
    assert not check_results[
        "test_not_in_features"
    ], f"There are tests that aren't in feature files: {check_results['test_not_in_features']}"
