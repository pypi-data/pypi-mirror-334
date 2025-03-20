import requests
from test_gen_framework.config import read_config
import base64

config = read_config()


def get_pr_diff(pr_number):
    url = f"https://api.github.com/repos/{config['REPO_OWNER']}/{config['REPO_NAME']}/pulls/{pr_number}/files"

    headers = {
        "Authorization": f"Bearer {config['GITHUB_TOKEN']}",
        "Accept": "application/vnd.github.v3+json",
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        files = response.json()
        pr_file_data = []

        for file in files:
            if file.get("patch"):
                file_data = {
                    "diff": file["patch"],
                    "filepathURL": file["contents_url"],
                    "localfilepath": file["filename"],
                }
                pr_file_data.append(file_data)

        return pr_file_data
    else:
        print(f"Error fetching PR diff: {response.status_code}")
        return None


def get_file_content(contents_url):
    headers = {
        "Authorization": f"Bearer {config['GITHUB_TOKEN']}",
        "Accept": "application/vnd.github.v3+json",
    }

    try:
        response = requests.get(contents_url, headers=headers)

        if response.status_code == 200:
            content_data = response.json()

            file_content = base64.b64decode(content_data.get("content")).decode("utf-8")

            return file_content
        else:
            print(
                f"Failed to fetch file content from {contents_url}. Status code: {response.status_code}"
            )
            return None
    except Exception as e:
        print(f"An error occurred while fetching the file content: {e}")
        return None
