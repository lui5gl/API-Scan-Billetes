import base64
from openai import OpenAI
from typing import Optional


class ScanImageModel:
    def __init__(self, image_base64: bytes, client: Optional[OpenAI] = None):
        """
        image_base64: contenido binario de la imagen (sin codificar)
        client: instancia opcional de OpenAI (se crea por defecto si no se pasa)
        """
        # Codificamos en base64
        self.image_base64 = base64.b64encode(image_base64).decode("utf-8")
        self.client = (
            client or OpenAI()
        )  # Usa el cliente proporcionado o crea uno nuevo

    def get_response(self) -> Optional[str]:
        try:
            completion = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": "Ayúdame a identificar si la imagen muestra un billete o no. Si no es un billete, indícalo claramente. Si sí es un billete, dime cuál es su denominación (por ejemplo, 20 pesos, 100 dólares, etc.) y describe su estado: si está en buen estado, regular o mal estado."},
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
            return completion.choices[0].message.content
        except Exception as e:
            print(f"❌ Error getting response from OpenAI: {e}")
            return None
