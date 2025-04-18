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
            with open(
                "ScanCashAPI/public/un_quetzal.png", "r", encoding="utf-8"
            ) as file:
                prompt = file.read()
                
        except FileNotFoundError:
            print("Error: No se encontró el archivo 'un_quetzal.png'")
            return None
        except Exception as e:
            print(f"Error al leer el archivo: {e}")
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
                                "text": prompt.strip(),
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
