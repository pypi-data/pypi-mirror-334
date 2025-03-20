import os
import shutil


def create_github_actions():
    gh_actions_dir = os.path.join(os.getcwd(), ".github", "workflows")
    os.makedirs(gh_actions_dir, exist_ok=True)

    package_dir = os.path.dirname(os.path.abspath(__file__))
    source_pipeline_file = os.path.join(package_dir, "ci.yml")

    destination_pipeline_file = os.path.join(gh_actions_dir, "ci.yml")

    if os.path.exists(source_pipeline_file):
        shutil.copy(source_pipeline_file, destination_pipeline_file)
        print(f"GitHub Actions pipeline created at: {destination_pipeline_file}")
    else:
        print(f"Error: ci.yml not found in {package_dir}")


def create_config_file():
    config_path = os.path.join(os.getcwd(), "config.yaml")
    config_content = """GITHUB_TOKEN: ""
    REPO_OWNER: ""
    REPO_NAME: ""
    PROJECT_NAME: ""
    TEST_LOC: ""
    IS_REPORTING: True
    CLOUD_TOKEN: ""
    """
    with open(config_path, "w") as file:
        file.write(config_content)


def init_config():
    create_github_actions()
    create_config_file()
