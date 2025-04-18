import datetime

from flask import Flask, jsonify, request
from models.scan_image_model import ScanImageModel

app = Flask(__name__)


@app.route("/", methods=["POST"])
def scanImage():
    if request.method != "POST":
        return "Method not allowed", 405

    if "image" not in request.files or request.files["image"] is None:
        return "No image provided", 400
    print("Request received at: " + str(datetime.datetime.now()))

    image = request.files["image"]
    scan_image_model = ScanImageModel(image_base64=image.read())

    response = scan_image_model.get_response()
    return jsonify({"response": response})


@app.route("/health", methods=["GET"])
def health():
    """
    Health check endpoint.
    :return: JSON response indicating the service is healthy.
    """
    return jsonify({"status": "ok"}), 200


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
