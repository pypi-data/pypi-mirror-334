REGRESSION_AUTOMATED_SUITES = {
    "IPAD": ({"automated", "regression", "suite"}, {"tablet", "all_ui"}),
    "IPHONE": ({"automated", "regression"}, {"phone", "all_ui"}),
    "ANDROID_TABLET": ({"automated", "regression", "android_adapted"}, {"tablet", "all_ui"}),
    "ANDROID_PHONE": ({"automated", "regression", "android_adapted"}, {"phone", "all_ui"}),
}

REGRESSION_AUTOMATED_RARE = {
    "IPAD": ({"automated", "rare"}, {"tablet", "all_ui"}),
    "IPHONE": ({"automated", "rare"}, {"phone", "all_ui"}),
    "ANDROID_TABLET": ({"automated", "rare", "android_adapted"}, {"tablet", "all_ui"}),
    "ANDROID_PHONE": ({"automated", "rare", "android_adapted"}, {"phone", "all_ui"}),
}

REGRESSION_AUTOMATED_OTHER = {
    "IPAD": ({"automated", "rare"}, {"all_platforms", "tablet", "all_ui"}),
    "IPHONE": ({"automated", "rare"}, {"all_platforms", "phone", "all_ui"}),
    "ANDROID_TABLET": ({"automated", "rare", "android"}, {"tablet", "all_ui"}),
    "ANDROID_PHONE": ({"automated", "rare", "android"}, {"phone", "all_ui"}),
}

REGRESSION_MANUAL_SUITES = {
    "IPAD": ({"manual", "regression"}, {"to_automate", "apple", "tablet", "all_ui"}),
    "IPHONE": ({"manual", "regression"}, {"to_automate", "apple", "phone", "all_ui"}),
    "ANDROID_TABLET": ({"manual", "regression"}, {"to_automate", "android", "all_platforms"}),
    "ANDROID_PHONE": ({"manual", "regression"}, {"to_automate", "android", "manual"}),
}

REGRESSION_TO_AUTOMATE_SUITES = {
    "IPAD": ({"to_automate", "regression"}, {"apple", "tablet", "all_ui", "@rare"}),
    "IPHONE": ({"to_automate", "regression"}, {"apple", "phone", "all_ui"}),
    "ANDROID_TABLET": ({"to_automate", "regression"}, {"android", "all_platforms", "@rare"}),
    "ANDROID_PHONE": ({"to_automate", "regression"}, {"android", "manual"}),
}

REGRESSION_MANUAL_RARE_SUITES = {
    "IPAD": ({"manual", "rare"}, {"apple", "tablet", "all_ui"}),
    "IPHONE": ({"manual", "rare"}, {"apple", "phone", "all_ui"}),
    "ANDROID_TABLET": ({"manual", "rare"}, {"android", "all_ui"}),
    "ANDROID_PHONE": ({"manual", "rare"}, {"android", "all_ui"}),
}

REGRESSION_TO_AUTOMATE_RARE_SUITES = {
    "IPAD": ({"to_automate", "rare"}, {"apple", "tablet", "all_ui"}),
    "IPHONE": ({"to_automate", "rare"}, {"apple", "phone", "all_ui"}),
    "ANDROID_TABLET": ({"to_automate", "rare"}, {"android", "all_ui"}),
    "ANDROID_PHONE": ({"to_automate", "rare"}, {"android", "all_ui"}),
}

REGRESSION_TESTS = {
    "IPAD": ({"regression"}, {"apple", "tablet", "all_ui", "all_platforms"}),
    "IPHONE": ({"regression"}, {"apple", "phone", "all_ui", "all_platforms"}),
    "ANDROID_TABLET": ({"regression"}, {"all_platforms", "android", "tablet", "all_ui"}),
    "ANDROID_PHONE": ({"regression"}, {"all_platforms", "android", "phone", "all_ui"}),
}

REGRESSION_TESTS_OTHER = {
    "IPAD": ({"regression", "apple"}, {"tablet", "all_ui"}),
    "IPHONE": ({"regression", "apple"}, {"phone", "all_ui"}),
    "ANDROID_TABLET": ({"regression", "android"}, {"tablet", "all_ui"}),
    "ANDROID_PHONE": ({"regression", "android"}, {"phone", "all_ui"}),
}

TO_AUTOMATE_TESTS = {
    "IPAD": ({"to_automate"}, {"productivity", "tablet", "all_ui"}),
    "IPHONE": ({"to_automate"}, {"productivity", "phone", "all_ui"}),
    "ANDROID_TABLET": ({"to_automate"}, {"all_platforms", "android", "tablet", "all_ui"}),
    "ANDROID_PHONE": ({"to_automate"}, {"all_platforms", "android", "phone", "all_ui"}),
}

ARCHIVE_TESTS = {
    "IPAD": ({"archive"}, {"all_platforms", "tablet", "all_ui"}),
    "IPHONE": ({"archive"}, {"all_platforms", "phone", "all_ui"}),
    "ANDROID_TABLET": ({"archive"}, {"all_platforms", "android", "tablet", "all_ui"}),
    "ANDROID_PHONE": ({"archive"}, {"all_platforms", "android", "phone", "all_ui"}),
}

ALL_AUTOMATED_TESTS = {
    "IPAD": ({"automated"}, {"apple", "tablet", "all_ui"}),
    "IPHONE": ({"automated"}, {"apple", "phone", "all_ui"}),
    "ANDROID_TABLET": ({"automated", "android_adapted"}, {"android", "tablet", "all_ui"}),
    "ANDROID_PHONE": ({"automated", "android_adapted"}, {"android", "phone", "all_ui"}),
}

ALL_MANUAL_TESTS = {
    "IPAD": ({"manual"}, {"productivity", "apple", "tablet", "all_ui"}),
    "IPHONE": ({"manual"}, {"productivity", "apple", "phone", "all_ui"}),
    "ANDROID_TABLET": ({"manual"}, {"all_platforms", "android", "tablet", "all_ui"}),
    "ANDROID_PHONE": ({"manual"}, {"all_platforms", "android", "phone", "all_ui"}),
}

WINDOWS_AND_MAC_TESTS = {
    "WINDOWS": ({"windows"}, {"productivity", "all_ui"}),
    "MAC_OS": ({"apple"}, {"productivity", "all_ui"}),
    "WINDOWS_ALL_PLATFORMS": ({"all_platforms"}, {"productivity", "all_ui"}),
    "MAC_OS_ALL_PLATFORMS": ({"all_platforms"}, {"productivity", "all_ui"}),
}

SUITE_TABLET_CASES = {
    "suite1": ({"automated", "suite1"}, {"tablet", "all_ui"}),
    "suite2": ({"automated", "suite2"}, {"tablet", "all_ui"}),
    "suite3": ({"automated", "suite3"}, {"tablet", "all_ui"}),
    "suite4": ({"automated", "suite4"}, {"tablet", "all_ui"}),
    "suite5": ({"automated", "suite5"}, {"tablet", "all_ui"}),
}

SUITE_PHONE_CASES = {
    "suite1": ({"automated", "suite1"}, {"phone", "all_ui"}),
    "suite2": ({"automated", "suite2"}, {"phone", "all_ui"}),
    "suite3": ({"automated", "suite3"}, {"phone", "all_ui"}),
    "suite4": ({"automated", "suite4"}, {"phone", "all_ui"}),
    "suite5": ({"automated", "suite5"}, {"phone", "all_ui"}),
}

REST_TESTS = {
    "AUTOMATED_REST_TEST": ({"automated"}, {"all_ui"}),
    "TO_AUTOMATED_REST_TEST": ({"to_automate"}, {"all_ui"}),
}

WEB_TESTS = {
    "AUTOMATED_WEB_TEST": ({"automated"}, {"all_ui"}),
    "TO_AUTOMATED_WEB_TEST": ({"to_automate"}, {"all_ui"}),
}
