import collections
import os
import sys
from copy import deepcopy
from datetime import datetime
from typing import List, Union

from gherkin.parser import Parser
from gherkin.token_scanner import TokenScanner

from Testrail_utils.pytest_testrail_api_client.modules.bdd_classes import TrFeature
from Testrail_utils.pytest_testrail_api_client.modules.exceptions import MissingSuiteInFeature

path_to_rep = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
)


def get_dict_from_locals(locals_dict: dict, replace_underscore: bool = False, exclude: list = None):
    exclude = ("self", "kwargs") if exclude is None else tuple(["self", "kwargs"] + exclude)
    result = {
        key if replace_underscore else key: value
        for key, value in locals_dict.items()
        if key not in exclude and "__py" not in key and value is not None
    }
    if "kwargs" in locals_dict:
        result.update(locals_dict["kwargs"])
    return result


def split_by_coma(*args):
    def sub_split(value):
        if value is not None:
            if not isinstance(value, (tuple, list)):
                value = trim(value).split(", ")
            return value

    if all([arg is None for arg in args]):
        return None
    elif len(args) > 1:
        return [sub_split(val) for val in args]
    else:
        return args[0].replace(" ", "").split(",") if not isinstance(args[0], (tuple, list)) else args[0]


def validate_id(status_id):
    if status_id is not None:
        if isinstance(status_id, (list, tuple)):
            return ",".join(tuple(map(str, status_id)))
        elif isinstance(status_id, str):
            return status_id.replace(" ", "")


def get_date_from_timestamp(date):
    return None if date is None else datetime.fromtimestamp(date)


# def is_main_loop(session: (Session, Config)):
#     if isinstance(session, Session):
#         if not hasattr(session.config, 'workerinput'):
#             return True
#         else:
#             return session.config.option.dist != "no"
#     else:
#         if not hasattr(session, 'workerinput'):
#             return True
#         else:
#             return session.option.dist != "no"


def get_worker_id(config):
    if hasattr(config, "config"):
        config = config.config
    return config.workerinput["workerid"] if hasattr(config, "workerinput") else "main"


def trim(string: str) -> str:
    return " ".join(string.split())


def get_features(path: str, test_rail):
    if path.endswith(".feature"):
        feature_files = [path]
    else:
        feature_files = tuple(
            f"{root}/{file}"
            for root, dirs, files in os.walk(path, topdown=False)
            for file in files
            if file.endswith(".feature")
        )
    feature_files = tuple(
        get_feature(feature_file, test_rail) for feature_file in feature_files if get_feature(feature_file, test_rail)
    )
    features = []
    suites_list = test_rail.suites.get_suites()
    tr_case_types = test_rail.configuration.type
    priority_list = test_rail.priorities._service_priorities()
    sections = {suite.id: test_rail.sections.get_sections(suite.id) for suite in suites_list}

    for feature in feature_files:
        parsed_feature = parse_feature(feature)
        suite_id = next(
            (suite.id for suite in suites_list if parsed_feature.main_suite == suite.name),
            None,
        )
        if suite_id is not None:
            parsed_feature.main_suite = suite_id
            parent_id = None
            for section in parsed_feature.sections:
                tr_section = next(
                    (sn for sn in sections[suite_id] if sn.name == section and sn.parent_id == parent_id),
                    None,
                )
                if tr_section is None:
                    parent_id = test_rail.sections.add_section(section, suite_id=suite_id, parent_id=parent_id).id
                else:
                    parent_id = tr_section.id
            parsed_feature.last_section = parent_id
        else:
            raise MissingSuiteInFeature(f"Missing suite in {feature}")
        validate_tags_in_feature(feature, test_rail)
        return_default_traceback()
        for scenario in parsed_feature.children:
            tags = list(tag["name"].lower().replace("@", "") for tag in scenario["scenario"]["tags"])
            tr_tags_from_case = get_tags(tags, test_rail)
            scenario["scenario"]["types"] = tr_case_types[tr_tags_from_case["case_type"][0]]
            scenario["scenario"]["priority"] = set_priority_by_type(tr_tags_from_case["case_type"][0], priority_list)
            scenario["scenario"]["custom_fields"] = set_custom_fields(
                tr_tags_from_case["case_automation_status"],
                tr_tags_from_case["case_ui_types"],
                tr_tags_from_case["case_platforms"],
                test_rail,
            )
            bugs = tuple(
                tag["name"].replace("@", "")
                for tag in scenario["scenario"]["tags"]
                if tag["name"].replace("@", "").startswith(test_rail.configuration.bug_prefix)
            )
            if len(bugs) > 0:
                scenario["scenario"]["refs"] = ",".join(bugs)
            else:
                scenario["scenario"]["refs"] = ""

        parsed_feature.children = sorted(
            parsed_feature.children,
            key=lambda scen: scen["scenario"]["location"]["line"],
        )
        features.append(parsed_feature)
    return features


def parse_feature(feature):
    examples_scenarios, to_delete = [], []
    for scenario in feature.children:
        if len(scenario["scenario"]["examples"]) > 0:
            examples = scenario["scenario"]["examples"][0]
            examples_names = tuple(var_name["value"] for var_name in examples["tableHeader"]["cells"])
            examples_values = []
            for var in tuple(var["cells"] for var in examples["tableBody"]):
                examples_values.append([y["value"] for y in var])
            for example in examples_values:
                sc = deepcopy(scenario)
                for index, name in enumerate(examples_names):
                    sc["scenario"]["name"] = sc["scenario"]["name"].replace(f"<{name}>", example[index])
                    for step in sc["scenario"]["steps"]:
                        if step.get("content", None) is None:
                            step["content"] = step["text"]
                        step["content"] = step["content"].replace(f"<{name}>", example[index])
                examples_scenarios.append(sc)
            to_delete.append(scenario)
    for scenario in to_delete:
        feature.children.remove(scenario)
    for scenario in examples_scenarios:
        feature.children.append(scenario)
    return feature


def get_feature(file_path: str, test_rail) -> TrFeature or None:
    try:
        with open(file_path, "r") as file:
            return TrFeature(
                Parser().parse(TokenScanner(file.read()))["feature"],
                file_path,
                test_rail,
            )
    except FileNotFoundError:
        return None


def _make_step(step: dict) -> dict:
    return {
        "content": f'**{step["keyword"].replace(" ", "")}:**{trim(step["text"])}',
        "expected": "",
    }


def _get_case_options(case_tags: list, tr_tags: dict, tr_case_types: dict, tr_priority: dict, test_rail):
    custom_fields, cases_type, priority = dict(), [], None
    for key, value in tr_tags.items():
        if key in case_tags:
            if value["type"] == "multi_select":
                if value["name"] in custom_fields:
                    custom_fields[value["name"]].append(int(value["id"]))
                else:
                    custom_fields[value["name"]] = [int(value["id"])]
            elif value["type"] in ("integer", "dropdown"):
                custom_fields[value["name"]] = int(value["id"])
            else:
                custom_fields[value["name"]] = value["id"]
    for key, value in test_rail.configuration.priority_replace.items():
        for val in value:
            if val.lower() in case_tags:
                priority = tr_priority[key.lower()]
                break
    if priority is None:
        priority = tr_priority["low"]
    for key, value in tr_case_types.items():
        if key in case_tags and key not in tr_tags:
            cases_type.append(value), case_tags.remove(key)

    return custom_fields, cases_type, priority


def replace_examples(where: str, examples: list, variables: str, all_vars: list):
    current_vars, variables = [], variables.lower()
    for var in all_vars:
        if all((x.lower() in variables for x in var)):
            current_vars = var
            break
    for index, param in enumerate(examples):
        if len(current_vars) > index:
            where = where.replace(f"<{param}>", current_vars[index])
    return where


def to_json(obj_list: List[object]) -> dict:
    return tuple(obj.to_json() if "to_json" in dir(obj) else obj.__dict__ for obj in obj_list)


def split_list(array: List[Union[tuple, list]], separator: int = 250) -> list:
    if isinstance(array, (tuple, list)):
        if isinstance(separator, int):
            if len(array) > 0:
                result, index = [], 0
                while True:
                    index_separator = index + separator
                    result.append(array[index:index_separator])
                    index += separator
                    if index > len(array):
                        break
                return result
            else:
                return []
        else:
            raise ValueError("separator must be integer")
    else:
        raise ValueError("array variable must be tuple or list")


def validate_variable(variable, var_types, var_name: str):
    if not isinstance(variable, var_types):
        raise ValueError(f"{var_name} must be {var_types}")


def _write_feature(file_path: str, line: int, column: int, value: str) -> None:
    def count_symbols(to_line: str, arr: list) -> int:
        return sum((len(length.encode()) for length in arr[:to_line]))

    with open(file_path, "r+") as file:
        lines = file.readlines()
        if os.name == "nt":
            lines[line - 1] = lines[line - 1][: column - 1] + f"{value} " + lines[line - 1][column - 1 :]
            file.seek(0)
            for line in lines:
                file.write(line)
            file.truncate()
            file.close()
        else:
            column = column - 1
            symbols_count = count_symbols(line - 1, lines) + column
            file.seek(symbols_count)
            rem = file.read()
            file.seek(symbols_count)
            file.write(f"{value} {rem}")


def sort_configurations(configuration: str, tr) -> str:
    config_split, config = trim(configuration).split(", "), []
    for param in tr.configs.get_configs():
        for suite in config_split:
            if suite.lower() in [conf.name.lower() for conf in param.configs]:
                config.append(suite)
    return ", ".join(config)


def validate_and_get_tag_value(all_tags_from_case, tag_category, test_rail):
    tag_categories_dict = {
        "automation_status": [*test_rail.configuration.automation_status.keys()],
        "type": [*test_rail.configuration.type.keys()],
        "ui_type": [*test_rail.configuration.ui_type.keys(), "all_ui"],
        "platform": [*test_rail.configuration.platform.keys(), "all_platforms"],
    }
    category_tag_list = tag_categories_dict[tag_category]
    result_tags = []
    category_without_suite_tag = []
    if "suite" in category_tag_list:
        for cat_tag in category_tag_list:
            if "suite" != cat_tag:
                category_without_suite_tag.append(cat_tag)
    else:
        category_without_suite_tag = category_tag_list
    exception = ""
    for tag in category_tag_list:
        for test_tag in all_tags_from_case:
            if tag == test_tag:
                result_tags.append(tag)
            elif tag == test_tag[:5]:
                result_tags.append(tag)
    if len(result_tags) == 0 and (tag_category == "type" or tag_category == "automation_status"):
        exception = f'Required tag "{tag_category}" from {category_without_suite_tag} is not present'
    elif len(result_tags) == 1 and tag_category == "automation_status":
        if "suite" in result_tags:
            exception = f'Required tag "{tag_category}" from {category_without_suite_tag} is not present'
    elif len(result_tags) > 1 and tag_category == "type":
        exception = f'More than one tag "{tag_category}" from {category_without_suite_tag} please review'
    elif len(result_tags) > 1 and tag_category == "automation_status":
        if "suite" in result_tags:
            if len(result_tags) > 2 and (tag_category == "automation_status" or tag_category == "type"):
                exception = f'More than one tag "{tag_category}" from {category_without_suite_tag} please review'
        else:
            exception = f'More than one tag "{tag_category}" from {category_without_suite_tag} please review'

    elif len(result_tags) > 1 and (tag_category == "ui_type" or tag_category == "platform"):
        if "all_ui" in result_tags:
            exception = f'More than one "{tag_category}" tags present with "all_ui", please review'
        elif "all_platforms" in result_tags:
            exception = f'More than one "{tag_category}" tags present with "all_platforms", please review'
    return {"result_tag": result_tags, "exception_message": exception}


def set_priority_by_type(tr_test_type, tr_priority_list):
    priority_switcher = {
        "archive": tr_priority_list["low"],
        "rare": tr_priority_list["medium"],
        "regression": tr_priority_list["high"],
        "critical": tr_priority_list["critical"],
        "smoke": tr_priority_list["high"],
    }
    return priority_switcher[tr_test_type]


def set_custom_fields(auto_status, ui_types, platforms, test_rail):
    automation_status_tr_ids = test_rail.configuration.automation_status
    ui_type_tr_ids = test_rail.configuration.ui_type
    platform_tr_ids = test_rail.configuration.platform

    def set_multiselect_fields_values(field_options, option_tr_ids):
        result = []
        if len(field_options) == 0:
            pass
        elif len(field_options) == 1 and "all" in field_options[0]:
            result = [*option_tr_ids.values()]
        else:
            for option in field_options:
                result.append(int(option_tr_ids[option]))
        return result

    result_fields_dict = {
        "custom_automation_type": int(automation_status_tr_ids[auto_status[0]]),
        "custom_ui_type": set_multiselect_fields_values(ui_types, ui_type_tr_ids),
        "custom_platform": set_multiselect_fields_values(platforms, platform_tr_ids),
    }

    return result_fields_dict


def hide_traceback():
    sys.tracebacklimit = 0


def return_default_traceback():
    sys.tracebacklimit = 1000


def validate_tags_in_feature(parsed_feature, test_rail):
    feature_exception_list = []
    print("\033[32m Please wait until feature validation is complete(could be ~ 1-2 min)\033[0m")
    tr_cases_list = {parsed_feature.main_suite: test_rail.cases.get_cases(suite_id=parsed_feature.main_suite)}
    all_tr_ids_from_feature_file = []
    for scenario in parsed_feature.children:

        def validate_tr_ids_for_feature():
            exception_list = []
            all_valid_ids_from_tr = [str(case.id) for case in tr_cases_list[parsed_feature.main_suite]]
            sc = scenario["scenario"]
            if "Outline" in sc["keyword"]:
                max_count_of_tr_ids = len(sc["examples"][0]["tableBody"])
            else:
                max_count_of_tr_ids = 1
            sc_tags = [tag["name"] for tag in sc["tags"]]
            sc_ids = [tag.replace("@C", "") for tag in sc_tags if "@C" in tag]
            all_tr_ids_from_feature_file.extend(sc_ids)
            invalid_ids = []
            duplicated_ids = [item for item, count in collections.Counter(sc_ids).items() if count > 1]
            if len(duplicated_ids) != 0:
                exception_list.append(
                    f'\033[35m Please review TR ids for \033[33m {scenario["scenario"]["name"]}, \033[0;31m duplicated ids:{duplicated_ids}, \033[0m line - {scenario["scenario"]["location"]["line"] - 1}\033[0m'
                )

            if len(sc_ids) != 0:
                for sc_id in sc_ids:
                    if sc_id not in all_valid_ids_from_tr:
                        invalid_ids.append(str(sc_id))

            if len(invalid_ids) > 0:
                exception_list.append(
                    f'\033[35m Please review TR ids for \033[33m {scenario["scenario"]["name"]}, \033[0;31m invalid ids:'
                    f'{invalid_ids}, \033[34m line - {scenario["scenario"]["location"]["line"] - 1} \033[0m'
                )

            if len(sc_ids) > max_count_of_tr_ids:
                exception_list.append(
                    f'\033[35m Amount of TR ids more than {max_count_of_tr_ids} for \033[33m {scenario["scenario"]["name"]}, \033[34m line - {scenario["scenario"]["location"]["line"] - 1} \033[0m'
                )

            if len(exception_list) > 0:
                feature_exception_list.append(list(set(exception_list)))

        def validate_and_get_tags():
            # first level validation
            tags = list(tag["name"].lower().replace("@", "") for tag in scenario["scenario"]["tags"])
            case_type = validate_and_get_tag_value(tags, "type", test_rail)
            case_automation_status = validate_and_get_tag_value(tags, "automation_status", test_rail)
            case_ui_types = validate_and_get_tag_value(tags, "ui_type", test_rail)
            case_platforms = validate_and_get_tag_value(tags, "platform", test_rail)
            exception_list = []
            for field in [
                case_type,
                case_automation_status,
                case_ui_types,
                case_platforms,
            ]:
                if field["exception_message"] != "":
                    exception_list.append(
                        f"\033[31m {field['exception_message']} for scenario \033[33m {scenario['scenario']['name']} "
                        f"\033[34m line - {scenario['scenario']['location']['line'] - 1} \033[0m"
                    )

            # second level validation check combination of platform + ui_type
            case_ui_types = case_ui_types["result_tag"]
            case_platforms = case_platforms["result_tag"]

            if len(case_ui_types) == 0 and len(case_platforms) == 0:
                pass
            elif "automated" in tags and any(tag in tags for tag in ["regression", "critical", "smoke"]):
                if (
                        "suite" not in case_automation_status["result_tag"]
                        and "android" not in tags
                        and "android_adapted" not in tags
                ):
                    exception_list.append(
                        f"\033[32m  Add 'suite' tag "
                        f"for scenario \033[33m {scenario['scenario']['name']} \033[34m line - "
                        f"{scenario['scenario']['location']['line'] - 1} \033[0m"
                    )
            elif (
                "automated" in tags and "regression" not in tags and "smoke" not in tags and "critical" not in tags
            ) or (
                "automated" not in tags and "regression" not in tags and "smoke" not in tags and "critical" not in tags
            ):
                if "suite" in case_automation_status["result_tag"]:
                    exception_list.append(
                        f"\033[94m  Remove 'suite' tag "
                        f"from scenario \033[33m {scenario['scenario']['name']} \033[34m line - "
                        f"{scenario['scenario']['location']['line'] - 1} \033[0m"
                    )
            elif len(case_ui_types) != 0 and len(case_platforms) == 0:
                exception_list.append(
                    f"\033[32m  Tags from 'ui_type' category specified without 'platform' tag, works only in pair "
                    f"for scenario \033[33m {scenario['scenario']['name']} \033[34m line - "
                    f"{scenario['scenario']['location']['line'] - 1} \033[0m"
                )
            elif len(case_ui_types) == 0 and len(case_platforms) != 0:
                exception_list.append(
                    f"\033[32m  Tags from 'platforms' category specified without 'ui_type' tag, works only in pair "
                    f"for scenario \033[33m {scenario['scenario']['name']} \033[34m line - "
                    f"{scenario['scenario']['location']['line'] - 1} \033[0m"
                )

            elif case_ui_types[0] == "all_ui" and len(case_platforms) == 0:
                exception_list.append(
                    f"\033[32m  If ui_type tag is 'all_ui', platform tags also should be specified and can not be "
                    f"empty for scenario \033[33m {scenario['scenario']['name']} \033[34m line - "
                    f"{scenario['scenario']['location']['line'] - 1} \033[0m"
                )
            elif len(case_ui_types) == 0 and case_platforms[0] == "all_platforms":
                exception_list.append(
                    f"\033[32m  If platform tag is 'all_platforms' tag, ui_type tags also should be specified and "
                    f"can not be empty for scenario \033[33m {scenario['scenario']['name']} \033[34m line - "
                    f"{scenario['scenario']['location']['line'] - 1} \033[0m"
                )
            else:
                validation_dict_platform_by_ui_type = {
                    "phone": ["android", "apple"],
                    "tablet": ["android", "apple"],
                    "productivity": ["apple", "windows"],
                    "all_ui": ["android", "apple", "windows", "all_platforms"],
                }

                validation_dict_ui_by_platform = {
                    "apple": ["phone", "tablet", "productivity", "all_ui"],
                    "android": ["phone", "tablet"],
                    "windows": ["productivity"],
                    "all_platforms": ["phone", "tablet", "productivity", "all_ui"],
                }

                available_ui_types_for_platforms_in_case = []
                for platform in case_platforms:
                    available_ui_types_for_platforms_in_case.extend(validation_dict_ui_by_platform[platform])

                if (
                    "productivity" in available_ui_types_for_platforms_in_case
                    and "phone" in available_ui_types_for_platforms_in_case
                    and "tablet" in available_ui_types_for_platforms_in_case
                ):
                    available_ui_types_for_platforms_in_case.append("all_ui")
                available_ui_types_for_platforms_in_case = list(set(available_ui_types_for_platforms_in_case))
                for ui_type in case_ui_types:
                    if ui_type in available_ui_types_for_platforms_in_case:
                        pass
                    else:
                        exception_list.append(
                            f'\033[35m  For specified "platforms": \033[32m {case_platforms} '
                            f"\033[35m available values: \033[32m {available_ui_types_for_platforms_in_case}"
                            f'\033[35m, but got:\033[31m {case_ui_types}, \033[33m {scenario["scenario"]["name"]}'
                            f'\033[34m line - {scenario["scenario"]["location"]["line"] - 1}  \033[0m'
                        )
                available_platforms_for_ui_in_case = []
                for ui_type in case_ui_types:
                    available_platforms_for_ui_in_case.extend(validation_dict_platform_by_ui_type[ui_type])
                if (
                    "apple" in available_platforms_for_ui_in_case
                    and "android" in available_platforms_for_ui_in_case
                    and "windows" in available_platforms_for_ui_in_case
                ):
                    available_platforms_for_ui_in_case.append("all_platforms")
                available_platforms_for_ui_in_case = list(set(available_platforms_for_ui_in_case))
                for platform in case_platforms:
                    if platform in available_platforms_for_ui_in_case:
                        pass
                    else:
                        exception_list.append(
                            f'\033[35m  For specified "ui_types": \033[32m {case_ui_types} '
                            f"\033[35m available values: \033[32m {available_platforms_for_ui_in_case}"
                            f'\033[35m, but got:\033[31m {case_platforms},\033[33m {scenario["scenario"]["name"]}'
                            f'\033[34m line - {scenario["scenario"]["location"]["line"] - 1}  \033[0m'
                        )

                if (
                    "productivity" in case_ui_types
                    and "phone" in case_ui_types
                    and "all_ui" not in case_ui_types
                    and "tablet" not in case_ui_types
                    and (
                        "android" in case_platforms
                        and "apple" in case_platforms
                        and "windows" in case_platforms
                        or "all_platforms" in case_platforms
                        or "android" in case_platforms
                        and "apple" in case_platforms
                        or "windows" in case_platforms
                        and "apple" in case_platforms
                        or "android" in case_platforms
                        and "windows" in case_platforms
                        or "apple" in case_platforms
                    )
                ):
                    exception_list.append(
                        f'\033[35m  Please also add tablet ui type tags \033[33m {scenario["scenario"]["name"]} '
                        f'\033[34m line - {scenario["scenario"]["location"]["line"] - 1}  \033[0m'
                    )

                exception_list = list(set(exception_list))
            feature_exception_list.append(exception_list)

        validate_and_get_tags()
        validate_tr_ids_for_feature()
    validation_result_dict = validate_tr_ids_duplications_in_features(
        parsed_feature, all_tr_ids_from_feature_file, test_rail
    )
    if len(validation_result_dict) > 0:
        feature_exception_list.append(
            [
                f"\033[35m TR ids in feature already present in another features: \033[0;31m {validation_result_dict} \033[0m"
            ]
        )
    hide_traceback()
    is_tags_without_issues = True
    for case_list in feature_exception_list:
        if len(case_list) > 0:
            is_tags_without_issues = False
            for ex_message in case_list:
                print(f"{ex_message}")
    if not is_tags_without_issues:
        raise Exception("Check tag validation!")
    print("\033[32m Validation passed ✅\033[0m Import processing ⏳")


def get_tags(tags, test_rail):
    case_type = validate_and_get_tag_value(tags, "type", test_rail)
    case_automation_status = validate_and_get_tag_value(tags, "automation_status", test_rail)
    case_ui_types = validate_and_get_tag_value(tags, "ui_type", test_rail)
    case_platforms = validate_and_get_tag_value(tags, "platform", test_rail)

    return {
        "case_type": case_type["result_tag"],
        "case_automation_status": case_automation_status["result_tag"],
        "case_ui_types": case_ui_types["result_tag"],
        "case_platforms": case_platforms["result_tag"],
    }


def validate_tr_ids_duplications_in_features(current_parsed_feature, all_id_from_current_feature, test_rail):
    def get_feature_paths(project_path):
        paths_list = []
        for root, dirs, files in os.walk(project_path):
            for file in files:
                if file.endswith(".feature"):
                    paths_list.append(os.path.join(root, file))
        return paths_list

    path_to_rep = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    paths_list = get_feature_paths(path_to_rep)
    paths_list = [path for path in paths_list if "archive" not in path]
    # remove current feature from list
    paths_list = [path for path in paths_list if current_parsed_feature.path not in path]
    result = {}
    for path in paths_list:
        try:
            feature = get_feature(path, test_rail)
        except Exception:
            pass
        current_feature_ids = []
        for scenario in feature.children:
            tags_dicts = scenario["scenario"]["tags"]
            all_scenario_tags = [tag["name"] for tag in tags_dicts]
            sc_ids = [tag.replace("@C", "") for tag in all_scenario_tags if "@C" in tag]
            current_feature_ids.extend(sc_ids)
        result[f"{feature.name}"] = current_feature_ids
    info_list = []
    for id in all_id_from_current_feature:
        for feature, values in result.items():
            for v in values:
                if id == v:
                    info_list.append({feature: id})

    result_dict = {}
    for dictionary in info_list:
        for key, value in dictionary.items():
            if key in result_dict:
                result_dict[key].append(value)
            else:
                result_dict[key] = [value]
    return result_dict
