from Load_tests.base_classes.load_tests_base_http_user_model import CABaseHttpUser, S3BaseHttpUser
from Load_tests.test_suites.content_on_sale_load_test_suite import TestSuiteContentOnSale
from Load_tests.test_suites.organization_load_test_suite import TestSuiteOrganization
from Load_tests.test_suites.sync_and_meta_load_test_suite import TestSuiteSyncMeta
from Load_tests.test_suites.tips_load_test_suite import TestSuiteTips


class LoadTestTips(CABaseHttpUser):
    tasks = [TestSuiteTips]


class LoadTestSyncMeta(CABaseHttpUser):
    tasks = [TestSuiteSyncMeta]


class LoadTestContentOnSale(S3BaseHttpUser):
    tasks = [TestSuiteContentOnSale]


class LoadTestOrganization(CABaseHttpUser):
    tasks = [TestSuiteOrganization]


if __name__ == "__main__":
    ...
