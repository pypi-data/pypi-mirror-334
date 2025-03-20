import random

from Testrail_utils.pytest_testrail_api_client.modules.case import Case
from Testrail_utils.pytest_testrail_api_client.service import _write_feature, get_features
from Testrail_utils.pytest_testrail_api_client.test_rail import TestRail


class TRTool(TestRail):
    def export_features_to_testrail(self, features):
        if isinstance(features, str):
            self.export_feature_to_testrail(features)
        elif isinstance(features, list):
            self.export_list_of_features_to_testrail(features)

    def export_list_of_features_to_testrail(self, list_of_features):
        for path in list_of_features:
            print(f"Exporting of the '{path}'")
            self.export_feature_to_testrail(path)

    def export_feature_to_testrail(self, abs_feature_file_path):
        features = get_features(abs_feature_file_path, self)
        cases_list = {
            suite: self.cases.get_cases(suite_id=suite) for suite in set(feature.main_suite for feature in features)
        }
        template_id = next(
            (
                template.id
                for template in self.templates.get_templates()
                if template.name == self.configuration.main_case_template_name
            ),
            None,
        )
        total_tests, current_test = sum((len(x.children) for x in features)), 1
        for feature in features:
            used_ids = []
            for scenario in feature.children:
                sc = scenario["scenario"]
                case = {
                    "section_id": feature.last_section,
                    "title": sc["name"],
                    "custom_steps_separated": sc["steps"],
                    "estimate": "5m",
                    "template_id": template_id,
                    "refs": sc["refs"],
                    **sc["custom_fields"],
                }
                if "priority" in sc:
                    case.update({"priority_id": sc["priority"]})
                if "types" in sc:
                    case.update({"type_id": sc["types"]})
                for field in self.configuration.skip_fields:
                    if field in case:
                        case.pop(field)
                current_scenario = Case(case)

                sc_tags = [tag["name"] for tag in sc["tags"]]
                sc_ids = [tag.replace("@C", "") for tag in sc_tags if "@C" in tag]
                validated_sc_ids = []
                for case_in_tr in cases_list[feature.main_suite]:
                    if str(case_in_tr.id) in sc_ids:
                        validated_sc_ids.append(str(case_in_tr.id))

                if len(validated_sc_ids) > 0:
                    if len(used_ids) == 0:
                        current_id = random.choice(validated_sc_ids)
                        used_ids.append(current_id)
                    else:
                        validated_sc_ids = [id for id in validated_sc_ids if id not in used_ids]
                        if len(validated_sc_ids) == 0:
                            current_id = ""
                        else:
                            current_id = random.choice(validated_sc_ids)
                            used_ids.append(current_id)
                else:
                    current_id = ""
                tr_case = next(filter(lambda x: str(x.id) == current_id, cases_list[feature.main_suite]), None)
                txt = f"scenario {current_scenario.title} in feature {feature.path}. {current_test} of {total_tests}"
                if tr_case is not None:
                    case.update({"case_id": tr_case.id})
                    case = self.cases.update_case(**case)
                    if not any((tag["name"].startswith(self.configuration.tr_prefix) for tag in sc["tags"])):
                        location = sc["tags"][0]["location"]
                        _write_feature(
                            feature.path,
                            location["line"],
                            location["column"],
                            self.configuration.tr_prefix + str(case.id),
                        )
                    if isinstance(case, str):
                        print(f"{txt}. Error {case}")
                    else:
                        print(f"\033[32m Updated {txt} \033[0m")
                else:
                    new_case = self.cases.add_case(**case)
                    if isinstance(new_case, str):
                        print(f"{txt}. Error {new_case}")
                    else:
                        print(f"\033[32m Upload new {txt} \033[0m")
                        location = sc["tags"][0]["location"]
                        _write_feature(
                            feature.path,
                            location["line"],
                            location["column"],
                            self.configuration.tr_prefix + str(new_case.id),
                        )
                current_test += 1
        print("Export completed")
