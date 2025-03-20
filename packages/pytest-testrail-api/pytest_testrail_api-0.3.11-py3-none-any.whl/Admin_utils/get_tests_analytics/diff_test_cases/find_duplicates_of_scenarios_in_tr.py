from typing import Dict, List, Tuple

from Admin_utils.get_tests_analytics.diff_test_cases.get_all_ids_cases_from_features import get_all_cases


def find_duplicates_of_scenarios_in_tr(tr_cases: Dict[int, Tuple[str, int]]) -> Dict[str, List[int]]:
    """
    The find_duplicates_of_scenarios_in_tr function retrieves all duplicate test cases from the TestRail project.
    """
    duplicates = {}
    for case_id, (
        case_name,
        section_id,
    ) in tr_cases.items():  # The function iterates over each test case in the tr_cases dictionary.
        if case_name not in duplicates:
            duplicates[case_name] = []
        duplicates[case_name].append(case_id)
    return {case_name: case_ids for case_name, case_ids in duplicates.items() if len(case_ids) > 1}


def main():
    all_scenarios = get_all_cases()
    duplicated_scenarios = find_duplicates_of_scenarios_in_tr(all_scenarios)
    print(duplicated_scenarios)


if __name__ == "__main__":
    main()
