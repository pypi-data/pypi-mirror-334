import requests
import json

CLOUD_API = "http://testgenaidash.test/syncTestData"


def sync_dashboard_view(data: json,):
    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(CLOUD_API, json=data, headers=headers)
        response.raise_for_status()
        return response.json()

    except requests.exceptions.RequestException as e:
        print(f"Error calling Dashboard webhook: {e}")
        return {"generated_code": ""}
