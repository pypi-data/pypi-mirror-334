from faker.generator import random
from locust import task

from Load_tests.base_classes.load_tests_base_test_suite_model import BaseTestSuite
from Rest.data_provider.common_data import SYNC_BODY


class TestSuiteSyncMeta(BaseTestSuite):
    sync_body = SYNC_BODY
    content_ids_dict = {}
    content_data_dict = {}

    def sync_request(self, content_type, sync_data):
        return self.client.post(f"/{content_type}/sync/", json=sync_data, headers=self.headers)

    def meta_request(self, content_type):
        ids_list = self.content_ids_dict.get(content_type)
        ids_list["updated"] = ids_list["updated"][: random.randint(50, 200)]
        return self.client.post(f"/{content_type}/meta/", json=ids_list, headers=self.headers)

    @task
    def sync_test(self):
        for content_type in self.content_types:
            sync_response = self.sync_request(content_type, self.sync_body)
            self.content_ids_dict.update({content_type: sync_response.json()})

    @task
    def meta_test(self):
        for content_type in self.content_types:
            meta_response = self.meta_request(content_type)
            self.content_data_dict.update({content_type: meta_response.json()})


if __name__ == "__main__":
    ...
