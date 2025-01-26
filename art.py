import time
import requests
import secrets
from datetime import datetime

class ART:
    def getImage(self, prompt):
        folder_id = secrets.folder_id
        api_key = secrets.api_key

        seed = int(round(datetime.now().timestamp()))

        body = {
            "modelUri": f"art://{folder_id}/yandex-art/latest",
            "generationOptions": {"seed": seed, "temperature": 0.6},
            "messages": [
                {"weight": 1, "text": prompt},
            ],
        }
        url = "https://llm.api.cloud.yandex.net/foundationModels/v1/imageGenerationAsync"
        headers = {"Authorization": f"Api-Key {api_key}"}

        response = requests.post(url, headers=headers, json=body)
        operation_id = response.json()["id"]

        url = f"https://llm.api.cloud.yandex.net:443/operations/{operation_id}"
        headers = {"Authorization": f"Api-Key {api_key}"}

        while True:
            response = requests.get(url, headers=headers)
            done = response.json()["done"]
            if done:
                break
            else:
                time.sleep(2)

        return response.json()["response"]["image"]