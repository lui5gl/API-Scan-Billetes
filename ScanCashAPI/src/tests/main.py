"""Python script to send an image to a Flask API and receive a response."""

import base64

import requests


def convert_image_to_base64(image_path):
    """
    Convierte una imagen a base64.
    :param image_path: Ruta de la imagen a convertir.
    :return: Cadena base64 de la imagen.
    """
    try:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")
    except FileNotFoundError:
        print(f"Error: No se encontró la imagen en '{image_path}'")
        return None


def send_image_to_api(image_path):
    """
    Envía una imagen a la API Flask y recibe la respuesta.
    :param image_path: Ruta de la imagen a enviar.
    :return: Respuesta de la API.
    """
    ENDPOINT = "http://localhost:5000"

    with open(image_path, "rb") as img_file:
        files = {"image": img_file}
        try:
            resp = requests.post(ENDPOINT, files=files, timeout=300_000)
        except requests.exceptions.RequestException as e:
            print("Error al conectar con la API:", e)
            return None

    if resp.status_code == 200:
        print("Image sent successfully!")
        return resp.json()
    else:
        print(f"Failed to send image. Status code: {resp.status_code}")
        return None


if __name__ == "__main__":
    IMG = "ScanCashAPI/public/un_quetzal.png"
    response = send_image_to_api(IMG)

    print(f"Response from API: {response}")
