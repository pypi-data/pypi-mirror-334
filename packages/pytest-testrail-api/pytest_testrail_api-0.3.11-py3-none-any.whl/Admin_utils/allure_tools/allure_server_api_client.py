import base64
import json
import os
from time import sleep

import requests

HOST = "https://allure-internal.nonprod.3d4medical.com/allure-docker-service"
ALLURE_USER = os.environ.get("ALLURE_USER")
ALLURE_PASSWORD = os.environ.get("ALLURE_PASSWORD")


class AllureSession:
    def __init__(self, host=HOST, user=ALLURE_USER, password=ALLURE_PASSWORD):
        self.host = host
        self.user = user
        self.password = password
        self._session = requests.Session()
        self.__get_auth()

    def __get_auth(self):
        self._session.headers.update({"Content-Type": "application/json", "accept": "*/*"})
        self._session.post(f"{self.host}/login", data=json.dumps({"username": self.user, "password": self.password}))
        self._session.headers.update({"X-CSRF-TOKEN": self._session.cookies.get("csrf_access_token")})


class AllureServerClient:
    @property
    def project(self):
        return ProjectApi()

    @property
    def action(self):
        return ActionApi()

    @staticmethod
    def send_report_to_allure_server(allure_project_id, allure_folder):

        def prepare_result_payload():
            results = []
            for file in os.listdir(allure_folder):
                if os.path.isfile(f"{allure_folder}/{file}"):
                    try:
                        with open(f"{allure_folder}/{file}", "rb") as jsonfile:
                            content = jsonfile.read()
                            if content.strip():
                                b64_content = base64.b64encode(content)
                                results.append({"file_name": file, "content_base64": b64_content.decode("UTF-8")})
                            else:
                                print("Empty File skipped: " + file)
                    finally:
                        jsonfile.close()

            return {"results": results}

        result_data = json.dumps(prepare_result_payload())
        response = AllureServerClient().action.send_results(project_id=allure_project_id, results_data=result_data)
        print(response["meta_data"]["message"])
        sleep(5)
        AllureServerClient().action.generate_report(project_id=allure_project_id)


class ActionApi(AllureSession):
    def get_allure_config(self):
        return self._session.get(url=f"{self.host}/config").json()

    def get_latest_report(self, project_id):
        params = {"project_id": project_id}
        return self._session.get(url=f"{self.host}/latest-report", params=params).json()

    def send_results(self, project_id, results_data):
        params = {"project_id": project_id}
        return self._session.post(url=f"{self.host}/send-results", params=params, data=results_data).json()

    def generate_report(
        self, project_id, execution_name="Drone daily run", execution_from="default", execution_type="default"
    ):
        params = {
            "project_id": project_id,
            "execution_name": execution_name,
            "execution_from": execution_from,
            "execution_type": execution_type,
        }
        self._session.get(url=f"{self.host}/generate-report", params=params)

    def clean_results(self, project_id):
        params = {"project_id": project_id}
        return self._session.get(url=f"{self.host}/clean-results", params=params).json()

    def clean_history(self, project_id):
        params = {"project_id": project_id}
        return self._session.get(url=f"{self.host}/clean-history", params=params).json()

    def render_emailable_report(self, project_id):
        params = {"project_id": project_id}
        return self._session.get(url=f"{self.host}/emailable-report/render", params=params).json()

    def export_emailable_report(self, project_id):
        params = {"project_id": project_id}
        return self._session.get(url=f"{self.host}/emailable-report/export", params=params).json()

    def export_report(self, project_id):
        params = {"project_id": project_id}
        return self._session.get(url=f"{self.host}/report/export", params=params).json()


class ProjectApi(AllureSession):
    def create_project(self, project_id):
        project_data = {"id": project_id}
        return self._session.post(f"{self.host}/projects", data=json.dumps(project_data)).json()

    def get_all_projects(self):
        return self._session.get(f"{self.host}/projects").json()

    def delete_project(self, project_id):
        return self._session.delete(f"{self.host}/projects/{project_id}").json()

    def get_project(self, project_id):
        return self._session.get(f"{self.host}/projects/{project_id}").json()

    def get_reports_for_project(self, project_id, path, redirect=False):
        params = {"redirect": redirect}
        return self._session.get(url=f"{self.host}/projects/{project_id}/reports/{path}", params=params).json()

    def search_project(self, project_id):
        params = {"id": project_id}
        return self._session.get(url=f"{self.host}/projects/search", params=params).json()
