from Load_tests.test_classes.load_tests import (
    LoadTestContentOnSale,
    LoadTestOrganization,
    LoadTestSyncMeta,
    LoadTestTips,
)

TESTS_MAP = {
    "sync and meta": LoadTestSyncMeta,
    "tips": LoadTestTips,
    "organization": LoadTestOrganization,
    "content on sale": LoadTestContentOnSale,
}
