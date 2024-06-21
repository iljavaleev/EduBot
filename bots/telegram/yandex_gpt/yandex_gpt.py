import json
import os

import aiohttp
from dotenv import load_dotenv
from utils.utils import get_template

load_dotenv()
template = get_template('question_templates/gpt_context_templates.j2')


class YaGPT:

    def __init__(self, university: str, question: str):
        self.university = university

        self.question = question

        self.headers = {
            'Authorization': f'Api-Key {os.getenv("GPT_TOKEN")}',
            'x-folder-id': f'{os.getenv("FOLDER_ID")}',
            'Content-type': 'application/json'
        }

        self.url = ('https://llm.api.cloud.yandex.net'
                    '/foundationModels/v1/completion')

        self.payload = {
            "modelUri": f"gpt://{os.getenv('FOLDER_ID')}/yandexgpt-lite",
            "completionOptions": {
                "stream": False,
                "temperature": 0.3,
                "maxTokens": "5000"
            },
            "messages": [
                {
                    "role": "system",
                    "text": template.render(role="system")
                },
                {
                    "role": "user",
                    "text": template.render(role="user")
                },
                {
                    "role": "assistant",
                    "text": template.render(role="assistant1")
                },
                {
                    "role": "user",
                    "text": f"{university}"
                },
                {
                    "role": "assistant",
                    "text": template.render(role="assistant2")
                },
                {
                    "role": "user",
                    "text": f"{question}"
                }
            ]
        }

    async def get_answer(self) -> str:
        async with aiohttp.ClientSession(
                headers=self.headers) as session:

            async with session.post(self.url,
                                    data=json.dumps(self.payload)) as response:
                if response.status == 200:
                    val = await response.json()
                else:
                    return "Извините, попробуйте задать вопрос позже"
        return val.get('result').get('alternatives')[0].get('message')['text']
