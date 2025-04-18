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
            completion = self.client.chat.completions.create(
                model="gpt-4.1-mini",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": """
                                        <prompt>
                                            <description>
                                                Identifica la denominación y la calidad de un billete.
                                            </description>

                                            <language>es</language>

                                            <rules>
                                                <rule id="1">Solo se aceptan billetes de Guatemala.</rule>
                                                <rule id="2">La respuesta debe ser breve, concisa y sin información adicional, comentarios,
                                                    abreviaciones, siglas, jerga, lenguaje técnico, coloquial, ofensivo, ambiguo ni
                                                    redundante.</rule>
                                                <rule id="3">La calidad del billete debe indicarse como: "bueno", "regular" o "malo".</rule>
                                                <rule id="4">La respuesta debe incluir la denominación y la calidad del billete.</rule>
                                                <rule id="5">Si el billete no es de Guatemala, responde: "No es un billete de Guatemala".</rule>
                                                <rule id="6">Si el billete es de Guatemala pero no se puede identificar, responde: "No se
                                                    puede identificar el billete".</rule>
                                            </rules>

                                            <denominations>
                                                <denomination>1 quetzal</denomination>
                                                <denomination>5 quetzales</denomination>
                                                <denomination>10 quetzales</denomination>
                                                <denomination>20 quetzales</denomination>
                                                <denomination>50 quetzales</denomination>
                                                <denomination>100 quetzales</denomination>
                                                <denomination>200 quetzales</denomination>
                                            </denominations>

                                            <qualities>
                                                <quality>bueno</quality>
                                                <quality>regular</quality>
                                                <quality>malo</quality>
                                            </qualities>

                                            <output_format>
                                                <expected>Es un billete de [denominación] en [calidad].</expected>
                                                <invalid_foreign>No es un billete de Guatemala.</invalid_foreign>
                                                <invalid_unknown>No se puede identificar el billete.</invalid_unknown>
                                            </output_format>

                                            <examples>
                                                <example>
                                                    <question>¿Qué billete es este?</question>
                                                    <answer>Es un billete de 100 quetzales en buen estado.</answer>
                                                </example>
                                                <example>
                                                    <question>¿Qué billete es este?</question>
                                                    <answer>No es un billete de Guatemala.</answer>
                                                </example>
                                            </examples>

                                            <error_handling>
                                                Si la información no es suficiente para determinar la denominación o la calidad, responde:
                                                "No se puede identificar el billete".
                                            </error_handling>

                                            <response_schema>
                                                <field name="origen">guatemala / extranjero / desconocido</field>
                                                <field name="denominacion">string o null</field>
                                                <field name="calidad">bueno / regular / malo / null</field>
                                            </response_schema>
                                        </prompt>
                                        """,
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
