import os
import re

from Admin_utils.get_tests_analytics.all_tags import (
    ALL_AUTOMATED_TESTS,
    ALL_MANUAL_TESTS,
    ARCHIVE_TESTS,
    REGRESSION_AUTOMATED_OTHER,
    REGRESSION_AUTOMATED_RARE,
    REGRESSION_AUTOMATED_SUITES,
    REGRESSION_MANUAL_RARE_SUITES,
    REGRESSION_MANUAL_SUITES,
    REGRESSION_TESTS,
    REGRESSION_TESTS_OTHER,
    REGRESSION_TO_AUTOMATE_RARE_SUITES,
    REGRESSION_TO_AUTOMATE_SUITES,
    REST_TESTS,
    SUITE_PHONE_CASES,
    SUITE_TABLET_CASES,
    TO_AUTOMATE_TESTS,
    WEB_TESTS,
    WINDOWS_AND_MAC_TESTS,
)
from Admin_utils.get_tests_analytics.diff_test_cases.get_all_ids_cases_from_features import get_feature_paths
from Testrail_utils.config import PROJECT_DIRECTORY
from Testrail_utils.pytest_testrail_api_client import test_rail
from Testrail_utils.pytest_testrail_api_client.service import get_feature

# ______You need to indicate project here______
PROJECT_CONFIG = os.environ.get("PROJECT_CONFIG", "App")

file_path = get_feature_paths(PROJECT_DIRECTORY[PROJECT_CONFIG])
all_tags = []

# Test suites for a specific test type
all_regression_tests = [REGRESSION_TESTS, REGRESSION_TESTS_OTHER]
to_automate_tests = [TO_AUTOMATE_TESTS]
all_automated_tests = [ALL_AUTOMATED_TESTS]
all_manual_tests = [ALL_MANUAL_TESTS]
archive_tests = [ARCHIVE_TESTS]
windows_and_apple_tests = [WINDOWS_AND_MAC_TESTS]
regression_automated_cases = [REGRESSION_AUTOMATED_SUITES, REGRESSION_AUTOMATED_RARE, REGRESSION_AUTOMATED_OTHER]
regression_manual_cases = [
    REGRESSION_MANUAL_SUITES,
    REGRESSION_TO_AUTOMATE_SUITES,
    REGRESSION_MANUAL_RARE_SUITES,
    REGRESSION_TO_AUTOMATE_RARE_SUITES,
]
smoke_cases = []
all_automated_broken_tests = []
suite_cases = [SUITE_TABLET_CASES, SUITE_PHONE_CASES]
rest_tests = [REST_TESTS]
web_tests = [WEB_TESTS]

# Test suites for each project
list_of_suites = {
    "App": {
        "ALL REGRESSION TESTS": all_regression_tests,
        "REGRESSION AUTOMATED CASES": regression_automated_cases,
        "CASES WITH SUITE TAG": suite_cases,
        "REGRESSION MANUAL CASES": regression_manual_cases,
        "ALL AUTOMATED TESTS": all_automated_tests,
        "TO AUTOMATE TESTS": to_automate_tests,
        "ALL MANUAL TESTS": all_manual_tests,
        "ARCHIVE TESTS": archive_tests,
        "WINDOWS_AND_MAC_TESTS": windows_and_apple_tests,
    },
    "Rest": {"REST_TESTS": rest_tests},
    "Web": {"WEB_TESTS": web_tests},
}.get(PROJECT_CONFIG)

# If you need to exclude some conclusions
conditions = [
    REGRESSION_AUTOMATED_RARE,
    REGRESSION_AUTOMATED_OTHER,
    REGRESSION_TESTS,
    TO_AUTOMATE_TESTS,
    ARCHIVE_TESTS,
    REGRESSION_MANUAL_RARE_SUITES,
    REGRESSION_TO_AUTOMATE_RARE_SUITES,
    ALL_MANUAL_TESTS,
    ALL_AUTOMATED_TESTS,
]


def get_tags_scenario(suites):
    test_rail_client = test_rail.TestRail()
    for path in file_path:
        feature = get_feature(path, test_rail_client)
        if feature is not None:
            for scenario in feature.children:
                try:
                    tags_in_scenario = list(tag["name"].replace("@", "") for tag in scenario["scenario"]["tags"])
                except Exception:
                    pass
                if "C" not in tags_in_scenario[0]:
                    print(f"\033[91m{scenario['scenario']['name']}\033[0m test is missing from the test rail")
                elif SUITE_PHONE_CASES in suites:
                    all_tags.append([item for item in tags_in_scenario])
                elif SUITE_TABLET_CASES in suites:
                    all_tags.append([item for item in tags_in_scenario])
                else:
                    get_tags = [re.sub(r"suite\d", "suite", item) for item in tags_in_scenario]
                    all_tags.append(get_tags)


def get_test_cases(suites):
    get_tags_scenario(suites)
    all_test_suite = {
        "IPAD": [],
        "IPHONE": [],
        "ANDROID_TABLET": [],
        "ANDROID_PHONE": [],
        "WINDOWS": [],
        "MAC_OS": [],
        "WINDOWS_ALL_PLATFORMS": [],
        "MAC_OS_ALL_PLATFORMS": [],
        "AUTOMATED_REST_TEST": [],
        "TO_AUTOMATED_REST_TEST": [],
        "AUTOMATED_WEB_TEST": [],
        "TO_AUTOMATED_WEB_TEST": [],
    }
    all_suite_tag_cases = {"suite1": [], "suite2": [], "suite3": [], "suite4": [], "suite5": []}
    for suite in suites:
        if suite == REGRESSION_AUTOMATED_SUITES:
            print("\033[95mRegression automated tests except rare cases\033[0m")
        elif suite == REGRESSION_MANUAL_SUITES:
            print("\033[95mRegression manual tests except rare cases\033[0m")
        elif suite == REGRESSION_TO_AUTOMATE_SUITES:
            print("\033[95mRegression to_automate tests except rare cases\033[0m")
        elif suite == SUITE_TABLET_CASES:
            print("\033[95mTablet test cases with suite tag\033[0m")
        elif suite == SUITE_PHONE_CASES:
            print("\033[95mPhone test cases with suite tag\033[0m")
        elif suite == WINDOWS_AND_MAC_TESTS:
            print("\033[95mWindows and Mac test cases with suite tag\033[0m")
        for name, type_of_tags in suite.items():
            test_suite = []
            include_tags, exclude_tags = type_of_tags
            for test in all_tags:
                if PROJECT_CONFIG == "App":
                    if suite in [ARCHIVE_TESTS, ALL_AUTOMATED_TESTS]:
                        if include_tags.issubset(set(test)) and exclude_tags.intersection(set(test)):
                            [test_suite.append(tag) for tag in test if re.compile(r"^C\d+").match(tag)]
                    else:
                        if (
                            include_tags.issubset(set(test))
                            and exclude_tags.intersection(set(test))
                            and "archive" not in set(test)
                        ):
                            [test_suite.append(tag) for tag in test if re.compile(r"^C\d+").match(tag)]
                else:
                    if (
                        include_tags.issubset(set(test))
                        and exclude_tags.isdisjoint(set(test))
                        and "archive" not in set(test)
                    ):
                        [test_suite.append(tag) for tag in test if re.compile(r"^C\d+").match(tag)]
            if suite in [SUITE_PHONE_CASES, SUITE_TABLET_CASES]:
                [all_suite_tag_cases[name].append(tag) for tag in test_suite]
            else:
                [all_test_suite[name].append(tag) for tag in test_suite]

            if suite in (REGRESSION_TO_AUTOMATE_SUITES, REGRESSION_MANUAL_SUITES, REGRESSION_AUTOMATED_SUITES):
                print(f"\033[1;91m{name} {len(set(test_suite))} tests:\033[0m {set(test_suite)}")
            if any(condition in suites for condition in conditions):
                pass
            else:
                print(f"\033[1;91m{name} {len(set(test_suite))} tests:\033[0m {set(test_suite)}")

    print("\033[93;1mAll tests: \033[0m")
    if len(all_test_suite.get("IPAD")) > 0:
        [
            print(f"🔖\033[1;94m{name} {len(set(tags))} tests:\033[0m {set(tags)}")
            for name, tags in list(all_test_suite.items())[:-4]
        ]

    if len(all_test_suite.get("WINDOWS")) > 0:
        [
            print(f"🔖\033[1;94m{name} {len(set(tags))} tests:\033[0m {set(tags)}")
            for name, tags in list(all_test_suite.items())[-4:]
        ]

        WINDOWS_SUM = sum(
            [
                len(set(tags))
                for name, tags in list(all_test_suite.items())[-4:]
                if name in ["WINDOWS", "WINDOWS_ALL_PLATFORMS"]
            ]
        )
        MAC_SUM = sum(
            [
                len(set(tags))
                for name, tags in list(all_test_suite.items())[-4:]
                if name in ["MAC_OS", "MAC_OS_ALL_PLATFORMS"]
            ]
        )

        [
            print(f"🔖\033[1;94m{str(name)}: \033[91m{sum}")
            for name, sum in (("WINDOWS_SUM", WINDOWS_SUM), ("MAC_SUM", MAC_SUM))
        ]

    elif PROJECT_CONFIG == "App":
        [
            print(f"🔖\033[1;94m{name} {len(set(tags))} tests:\033[0m {set(tags)}")
            for name, tags in all_suite_tag_cases.items()
        ]
        all_suite_tag_tests = 0
        for name, tags in all_suite_tag_cases.items():
            all_suite_tag_tests += len(set(tags))
        [all_suite_tag_tests + len(set(tags)) for name, tags in all_suite_tag_cases.items()]
        print(f"📄\033[1;94mAll cases tablet+phone with suite cases: {all_suite_tag_tests}\033[0m")


def print_result():
    for name, tags in list_of_suites.items():
        print(f"ℹ️ \033[92m{name} \033[0m")
        get_test_cases(tags)


if __name__ == "__main__":
    print_result()
