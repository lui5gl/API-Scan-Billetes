from flask import Flask, jsonify, request
from openai import OpenAI

from models.scan_image_model import ScanImageModel

app = Flask(__name__)
client = OpenAI()


@app.route("/", methods=["POST"])
def scanImage():
    if request.method != "POST":
        return "Method not allowed", 405

    if "image" not in request.files:
        return "No image provided", 400

    image = request.files["image"]

    if image.filename == "":
        return "No image provided", 400

    scan_image_model = ScanImageModel(image_base64=image.read(), client=client)

    response = scan_image_model.get_response()

    return jsonify({"response": response})


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "healthy"}), 200


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
