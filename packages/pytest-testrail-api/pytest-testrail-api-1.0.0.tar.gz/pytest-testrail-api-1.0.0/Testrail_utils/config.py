import os

path_to_rep = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

TESTRAIL_URL = os.environ.get("TESTRAIL_URL", "https://3d4medical.testrail.net")
TESTRAIL_EMAIL = os.environ.get("TESTRAIL_EMAIL")
TESTRAIL_KEY = os.environ.get("TESTRAIL_KEY")

TESTRAIL_PATH_TO_CASE = f"{TESTRAIL_URL}/index.php?/cases/view"

PROJECT_DIRECTORY = {
    "App": f"{path_to_rep}/App",
    "Rest": f"{path_to_rep}/Rest",
    "Web": f"{path_to_rep}/Web",
    "Sdk": f"{path_to_rep}/SDK",
    "Grasshopper": f"{path_to_rep}/Grasshopper",
}

TR_PROJECT_ID = {
    "App": os.environ.get("TR_PROJECT_ID_APP", 70),
    "Rest": os.environ.get("TR_PROJECT_ID_REST", 62),
    "Web": os.environ.get("TR_PROJECT_ID_WEB", 67),
    "Sdk": os.environ.get("TR_PROJECT_ID_SDK", 180),
    "Grasshopper": os.environ.get("TR_PROJECT_ID_GRASSHOPPER", 871),
}
