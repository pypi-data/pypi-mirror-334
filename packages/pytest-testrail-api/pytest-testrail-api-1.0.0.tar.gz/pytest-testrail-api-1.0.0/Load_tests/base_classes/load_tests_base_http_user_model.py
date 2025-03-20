from locust import HttpUser, between

from Rest.definitions import CA_API_VERSION, CA_URL


class BaseHttpUser(HttpUser):
    tasks = []
    abstract = True  # This is an abstract class and should not be used directly as it does not have any tasks
    min_wait = 1000
    max_wait = 2000
    # env = None
    wait_time = between(0, 0.5)


class CABaseHttpUser(BaseHttpUser):
    host = CA_URL + CA_API_VERSION
    abstract = True  # This is an abstract class and should not be used directly as it does not have any tasks


class S3BaseHttpUser(BaseHttpUser):
    host = "https://cdn.3d4medical.com/complete_anatomy-userdata"
    abstract = True  # This is an abstract class and should not be used directly as it does not have any tasks
