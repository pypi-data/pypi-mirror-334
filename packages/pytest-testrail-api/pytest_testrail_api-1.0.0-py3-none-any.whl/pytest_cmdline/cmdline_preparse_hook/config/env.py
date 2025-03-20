import importlib.util
import os

from Admin_utils.custom_logger import logger
from App.config.driver_config import (
    ANDROID_PHONE_DEVICE_NAME,
    ANDROID_TABLET_DEVICE_NAME,
    APPIUM_PORT,
    IPAD_DEVICE_NAME,
    IPHONE_DEVICE_NAME,
    PLATFORM,
    PLATFORM_AND_APP,
)
from App.config.env import allure_data

"""A custom function like load_dotenv()"""


def load_env_from_py(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File {file_path} not found")

    spec = importlib.util.spec_from_file_location("env", file_path)
    env = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(env)

    for attr in dir(env):
        if not attr.startswith("__"):
            value = getattr(env, attr)
            if isinstance(value, (bool, int, float)):
                value = str(value)
            elif not isinstance(value, str):
                continue
            os.environ[attr] = value


APP_PROJECT_DIRECTORY = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

env_path = os.path.join(APP_PROJECT_DIRECTORY, "App", "config", "env.py")

if os.path.exists(env_path):
    load_env_from_py(env_path)
    logger.info(f"Loaded environment variables from {env_path}")
else:
    logger.error(f"Environment file {env_path} not found.")


def get(key, default=None):
    """
    Improved os.environ.get(key, default) for getting boolean values.
    Because by default the function returns boolean values in the form str()
    """
    var = os.environ.get(key=key, default=default)
    if isinstance(var, str):
        if var.lower() == "true":
            var = True
        elif var.lower() == "false":
            var = False
    return var


BROWSER = "chrome"  # browser name ["chrome", "edge", "firefox", "remote"]

CREATE_ALLURE_REPORT, ALLURE_REPORT_PATH = allure_data()
# CREATE_ALLURE_REPORT = get("CREATE_ALLURE_REPORT")
# ALLURE_REPORT_PATH = get("ALLURE_REPORT_PATH", os.path.join(APP_PROJECT_DIRECTORY, "App", "config"))
PLATFORM_AND_APP = get("PLATFORM_AND_APP", PLATFORM_AND_APP)
PLATFORM = get("PLATFORM", PLATFORM)
APPIUM_PORT = get("APPIUM_PORT", APPIUM_PORT)
IPAD_DEVICE_NAME = get("IPAD_DEVICE_NAME", IPAD_DEVICE_NAME)
IPHONE_DEVICE_NAME = get("IPAD_DEVICE_NAME", IPHONE_DEVICE_NAME)
ANDROID_PHONE_DEVICE_NAME = get("IPAD_DEVICE_NAME", ANDROID_PHONE_DEVICE_NAME)
ANDROID_TABLET_DEVICE_NAME = get("IPAD_DEVICE_NAME", ANDROID_TABLET_DEVICE_NAME)
