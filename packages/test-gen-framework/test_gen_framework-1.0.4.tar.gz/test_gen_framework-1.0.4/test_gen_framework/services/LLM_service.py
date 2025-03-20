import requests

LLM_API_URL = "http://easy-yak-unique.ngrok-free.app/predict"


def call_llm_model(prompt: str) -> dict:
    headers = {"Content-Type": "application/json"}
    payload = {"input": prompt}

    try:
        response = requests.post(LLM_API_URL, json=payload, headers=headers)

        if response.status_code == 404:
            print("AI service is not available, try again later")
            return {"generated_code": ""}

        response.raise_for_status()

        return response.json()

    except requests.exceptions.RequestException as e:
        print(f"Error calling LLM API: {e}")
        return {"generated_code": ""}
