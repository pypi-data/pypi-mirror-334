import os


def set_pytest_plugins_by_os(path_to_project):
    plugins = []
    path_separator = chr(92) if os.name == "nt" else "/"
    for root, dirs, files in os.walk(os.path.join(path_to_project, "tests"), topdown=False):
        for file in files:
            if file.split(".")[0] == "steps_defs" and "pycache" not in root:
                plugins.append(
                    f"{root[root.find(f'{path_separator}tests') + 1:].replace(path_separator, '.')}.{file.split('.')[0]}"
                )
    return plugins
