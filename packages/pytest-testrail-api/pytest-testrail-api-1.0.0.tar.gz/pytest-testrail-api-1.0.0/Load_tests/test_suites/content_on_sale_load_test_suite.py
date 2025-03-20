from locust import task

from Load_tests.base_classes.load_tests_base_test_suite_model import BaseTestSuite

unauthorized_headers = {"Content-Type": "application/json"}


class TestSuiteContentOnSale(BaseTestSuite):
    def content_on_sale_request(self, method, headers=None):
        headers = headers or self.headers
        return self.client.request(method, "/content_on_sale.json", headers=headers)

    @task
    def get_content_on_sale_authorized_test(self):
        self.content_on_sale_request("get")

    @task
    def get_content_on_sale_unauthorized_test(self):
        headers = unauthorized_headers
        self.content_on_sale_request("get", headers=headers)

    @task(3)
    def head_content_on_sale_authorized_test(self):
        self.content_on_sale_request("head")

    @task(3)
    def head_content_on_sale_unauthorized_test(self):
        headers = unauthorized_headers
        self.content_on_sale_request("head", headers=headers)
