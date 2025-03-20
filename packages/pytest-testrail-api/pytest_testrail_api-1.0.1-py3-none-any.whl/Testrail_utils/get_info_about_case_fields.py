from Testrail_utils.pytest_testrail_api_client.test_rail import TestRail

if __name__ == "__main__":
    test_rail = TestRail()
    case_types = test_rail.case_types._service_case_types()
    custom_fields = test_rail.case_fields._service_case_fields()
    priority_list = test_rail.priorities._service_priorities()
    print(case_types)
    print(custom_fields)
    print(priority_list)
