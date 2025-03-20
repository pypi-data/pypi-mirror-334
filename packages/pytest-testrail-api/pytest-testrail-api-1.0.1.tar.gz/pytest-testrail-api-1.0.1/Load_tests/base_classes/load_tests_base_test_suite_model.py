from locust import SequentialTaskSet

from Rest.definitions import CONTENT_TYPES
from Rest.steps.login_steps import LoginSteps


class BaseTestSuite(SequentialTaskSet):
    content_types = CONTENT_TYPES
    headers = {
        "sessionid": LoginSteps.login("B2B Educator"),
        "Content-Type": "application/json",
    }

    @classmethod
    def update_sessionid(cls, new_sessionid):
        cls.headers.update({"sessionid": new_sessionid})

    # def on_start(self):
    #     self.update_sessionid(self.headers["sessionid"])
