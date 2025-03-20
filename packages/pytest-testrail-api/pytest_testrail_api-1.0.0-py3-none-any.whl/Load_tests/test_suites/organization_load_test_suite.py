from locust import task

from Load_tests.base_classes.load_tests_base_test_suite_model import BaseTestSuite


class TestSuiteOrganization(BaseTestSuite):
    def organization_request(self, headers=None):
        headers = headers or self.headers
        return self.client.get("/organization/", headers=headers)

    @task
    def organization_authorized_test(self):
        self.organization_request()

    @task
    def organization_unauthorized_test(self):
        headers = {
            "Content-Type": "application/json",
        }
        self.organization_request(headers=headers)
