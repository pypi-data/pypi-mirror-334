from Admin_utils.allure_tools.allure_server_api_client import AllureServerClient

if __name__ == "__main__":
    AllureServerClient().project.create_project("test")

    AllureServerClient().project.delete_project("test")
