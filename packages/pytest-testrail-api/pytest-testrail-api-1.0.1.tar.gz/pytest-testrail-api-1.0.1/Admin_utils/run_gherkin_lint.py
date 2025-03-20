import os
import subprocess
from pathlib import Path


def run_gherkin_lint(project_folder):
    get_linter = os.popen("npm list gherkin-lint").read()
    if "empty" in get_linter:
        os.system("npm i gherkin-lint")
    if os.name == "nt":
        path_to_linter = ""
    else:
        path_to_linter = f"{str(Path.home())}/node_modules/gherkin-lint/dist/main.js"

    folder_with_features = f"{os.path.dirname(os.path.dirname(__file__))}/{project_folder}/tests"
    linter_file = f"{os.path.dirname(os.path.dirname(__file__))}/.gherkin-lintrc"
    os.path.dirname(__file__)
    result = subprocess.run(
        ["node", f"{path_to_linter}", "-c", f"{linter_file}", f"{folder_with_features}"], stdout=subprocess.PIPE
    )
    if result.returncode == 0:
        print(f"gherkin-lint verifications of {project_folder} folder - OK")


if __name__ == "__main__":
    run_gherkin_lint(project_folder="App")
