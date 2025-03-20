import os

from tools.git_tools import GitTool
from tools.testrail_tool import TRTool

# Set the local environment variable EXPORTING_OPTION equal to "local", "commit" or "branch"
EXPORTING_OPTION = os.environ.get("EXPORTING_OPTION", "local")
PATH_TO_REP = os.path.dirname(os.path.dirname(__file__))


def export_scenarios_to_testrail(features):
    test_rail_client = TRTool()
    test_rail_client.export_features_to_testrail(features)


def main():
    """
    If you need to export a single feature file you should enter the 'abs_path_to_feature_file' as a string
    Otherwise, the script will export all updated feature files according to the 'EXPORTING_OPTION' variable
    """
    abs_path_to_feature_file = ""
    repo = GitTool(PATH_TO_REP)
    features_to_export = abs_path_to_feature_file or repo.get_updated_features(EXPORTING_OPTION)
    export_scenarios_to_testrail(features_to_export)


if __name__ == "__main__":
    main()
