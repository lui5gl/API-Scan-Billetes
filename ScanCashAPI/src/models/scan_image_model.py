import base64
import datetime
from typing import Optional

from openai import OpenAI

client = OpenAI()


class ScanImageModel:
    def __init__(self, image_base64: bytes):
        self.image_base64 = base64.b64encode(image_base64).decode("utf-8")
        self.client = client

    def get_response(self) -> Optional[str]:
        try:
            with open("ScanCashAPI/src/models/prompt.xml", "r", encoding="utf-8") as file:
                prompt = file.read()
        except FileNotFoundError:
            print("❌ Prompt file not found.")
            return None

        try:
            completion = self.client.chat.completions.create(
                model="gpt-4.1-mini",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": prompt,
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{self.image_base64}",
                                },
                            },
                        ],
                    }
                ],
            )
            print("Response sent in: " + str(datetime.datetime.now()))
            return completion.choices[0].message.content
        except Exception as e:
            print(f"❌ Error getting response from OpenAI: {e}")
            return None
