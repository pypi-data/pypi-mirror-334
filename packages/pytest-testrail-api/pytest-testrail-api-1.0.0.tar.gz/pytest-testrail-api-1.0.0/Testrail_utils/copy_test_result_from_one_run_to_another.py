from pytest_testrail_api_client.test_rail import TestRail

STATUS_ID = [1]
OVERWRITE_RESULTS = [3, 1]
"""
STATUS_ID - LIST variable for indicate which tests will be exported to new run. If more, that 1 - [1, 2, 4, ..]
OVERWRITE_RESULTS - LIST for overwrite test result in new run
1 - passed
2 - blocked
3 - untested
4 - retest
5 - failed
6 - not_applicable
7 - not_relevant
"""


def export_results(old_run_id, new_run_id):
    client = TestRail()
    client.service.copy_results_from_run(
        old_run_id=old_run_id, new_run_id=new_run_id, status_id=STATUS_ID, overwrite_results=OVERWRITE_RESULTS
    )
