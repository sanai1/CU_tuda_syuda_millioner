import time
import requests


class YandexText(object):
    folder_id = "b1gug7c74crq38i2spt2"
    api_key = "AQVN07CqobFnf6YA4f-LYwKCKqhJ_slTIzOgEWGf"
    gpt_model = 'yandexgpt-lite'
    system_prompt = 'Ты писатель. Напиши коротенький рассказ на данную тему. В ответ дай только текст.'

    def getAnswer(self, user_prompt) -> str:
        body = {
            'modelUri': f'gpt://{self.folder_id}/{self.gpt_model}',
            'completionOptions': {'stream': False, 'temperature': 0.3, 'maxTokens': 2000},
            'messages': [
                {'role': 'system', 'text': self.system_prompt},
                {'role': 'user', 'text': user_prompt},
            ],
        }
        url = 'https://llm.api.cloud.yandex.net/foundationModels/v1/completionAsync'
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Api-Key {self.api_key}'
        }

        response = requests.post(url, headers=headers, json=body)
        operation_id = response.json().get('id')

        url = f"https://llm.api.cloud.yandex.net:443/operations/{operation_id}"
        headers = {"Authorization": f"Api-Key {self.api_key}"}

        while True:
            response = requests.get(url, headers=headers)
            done = response.json()["done"]
            if done:
                break
            else:
                time.sleep(1)

        data = response.json()
        return data['response']['alternatives'][0]['message']['text']
