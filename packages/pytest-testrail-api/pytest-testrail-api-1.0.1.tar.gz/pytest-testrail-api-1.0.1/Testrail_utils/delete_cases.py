from pytest_testrail_api_client.test_rail import TestRail

from Testrail_utils.config import TR_PROJECT_ID


def delete_test_cases(cases_id: str):
    TestRail().service.delete_cases_by_regex(cases_id)


def move_cases_to_section(section_id: int, suite_id: int, case_ids: list):
    return TestRail().cases.move_cases_to_section(section_id=section_id, suite_id=suite_id, case_ids=case_ids)


def delete_sections(ids: list):
    for section_id in ids:
        TestRail().sections.delete_section(section_id)


def move_section(section_id: int, parent_id: int):
    TestRail().sections.move_section(section_id, parent_id)


if __name__ == "__main__":
    """
    indicate test rails cases id's for deleting in rails_ids variable.
    Function use regEx for take id from text
    """
    rails_ids = """@C113372 @C113373"""
    delete_test_cases(rails_ids)
    """
    indicate test rails sections id's for deleting in section_ids variable
    """
    section_ids = [25334]
    delete_sections(section_ids)
    """
    Moves a section to another suite or section
       :param#1 section_id: The ID of the section
       :param#2 parent_id:  The ID of the parent section (it can be null if it should be moved to the root).
                            Must be in the same project and suite. May not be direct child of the section being moved.
    """
    move_section_ids = [25336, 3998]
    if move_section_ids:
        move_section(move_section_ids[0], move_section_ids[1])

    """
    Moves cases to another suite or section.
        :param section_id: The ID of the section the case will be moved to.
        :param suite_id: The ID of the suite the case will be moved to.
        :param case_ids: A comma-separated list of case IDs
    """
    move_cases_to_section(section_id=3998, suite_id=TR_PROJECT_ID["Web"], case_ids=[])
