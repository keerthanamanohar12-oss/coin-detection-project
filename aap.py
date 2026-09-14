from flask import Flask, render_template, request, jsonify
import cv2
import os

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/detect", methods=["POST"])
def detect_coins():

    if "image" not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    file = request.files["image"]

    image_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(image_path)

    image = cv2.imread(image_path)

    if image is None:
        return jsonify({"error": "Unable to read image"}), 400

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (9, 9), 2)

    circles = cv2.HoughCircles(
        gray,
        cv2.HOUGH_GRADIENT,
        dp=1.2,
        minDist=30,
        param1=100,
        param2=25,
        minRadius=10,
        maxRadius=200
    )

    coin_count = 0

    if circles is not None:
        coin_count = len(circles[0])
        print("Detected circles:",circles)
    
    return jsonify({
        "count": coin_count
    })


if __name__ == "__main__":
    app.run(debug=True)