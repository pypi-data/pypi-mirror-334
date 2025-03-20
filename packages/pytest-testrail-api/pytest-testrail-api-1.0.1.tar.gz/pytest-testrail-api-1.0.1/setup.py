import setuptools
from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="pytest-testrail-api",
    version="1.0.1",
    use_scm_version=False,
    description="TestRail Api Python Client",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Yevhen Halitsyn",
    author_email="halitsyny@science.regn.net",
    packages=setuptools.find_packages(exclude=("tests", "dev_tools")),
    install_requires=["requests", "pytest", "gherkin-official>=4.1.0", "pytest-bdd>=3.3.0", "typing"],
    entry_points={
        "pytest11": [
            "pytest-testrail-api = pytest_testrail_api.configure",
        ],
        "testrail_api": ["test_rail_client = pytest_testrail_api.test_rail"],
    },
)
