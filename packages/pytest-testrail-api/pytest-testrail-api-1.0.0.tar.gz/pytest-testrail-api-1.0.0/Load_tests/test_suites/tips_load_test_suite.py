from locust import task

from Load_tests.base_classes.load_tests_base_test_suite_model import BaseTestSuite


class TestSuiteTips(BaseTestSuite):
    def tips_request(self, headers=None):
        headers = headers or self.headers
        return self.client.get("/tips/", headers=headers)

    @task
    def tips_authorized_test(self):
        self.tips_request()

    @task
    def tips_unauthorized_test(self):
        headers = {
            "Content-Type": "application/json",
        }
        self.tips_request(headers=headers)
