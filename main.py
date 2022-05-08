import base64
import io
import os
import imghdr
import uuid
import cv2
import numpy as np

from google.cloud import storage
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
from project import mosavid

# from PIL import Image

app = Flask(
    __name__,
    template_folder="project/templates",
    static_folder="project/static",
)

app.config["UPLOAD_EXTENSIONS"] = [".mp4", ".jpg", ".png", ".jpeg"]

TEMP_CONTENT_PATH = "/tmp"


def _file_is_valid(file: str) -> bool:
    filename = secure_filename(file)
    if filename == "":
        print("empty filename")
        return False

    file_ext = os.path.splitext(filename)[1]
    if file_ext not in app.config["UPLOAD_EXTENSIONS"]:
        print("file extension invalid")
        return False

    return True


@app.route("/")
def root():
    return render_template("index.html")


@app.route("/create_mosaic", methods=["POST"])
def create_mosaic():
    image = request.files["image"]
    video = request.files["video"]

    image_path = f"{TEMP_CONTENT_PATH}/{uuid.uuid1()}"
    video_path = f"{TEMP_CONTENT_PATH}/{uuid.uuid1()}"
    # image.save(f"/tmp/{image_path}")
    # video.save(f"/tmp/{video_path}")
    image.save(image_path)
    video.save(video_path)

    mosaic = mosavid.create_mosaic(image_path, video_path)
    mosaic_file_name = f"{uuid.uuid1()}.png"
    mosaic_file_path = f"{TEMP_CONTENT_PATH}/{mosaic_file_name}"
    cv2.imwrite(filename=mosaic_file_path, img=mosaic)

    return render_template("index.html", mosaic=mosaic_file_name)


if __name__ == "__main__":
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    # Flask's development server will automatically serve static files in
    # the "static" directory. See:
    # http://flask.pocoo.org/docs/1.0/quickstart/#static-files. Once deployed,
    # App Engine itself will serve those files as configured in app.yaml.
    TEMP_CONTENT_PATH = "project/static"
    app.run(host="127.0.0.1", port=5000, debug=True)
