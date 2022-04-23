import os
import imghdr

from google.cloud import storage
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename

app = Flask(
    __name__,
    template_folder="project/templates",
    static_folder="project/static",
)

app.config["UPLOAD_EXTENSIONS"] = [".mp4", ".jpg", ".png", ".jpeg"]


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


@app.route("/upload_video", methods=["POST"])
def upload_video():
    video = request.files["video"]

    if _file_is_valid(video.filename):
        storage_client = storage.Client()
        bucket = storage_client.lookup_bucket("mosavid.appspot.com")
        blob = bucket.blob(video.filename)
        blob.upload_from_file(video)

        return "", 204

    return "Invalid video", 400


@app.route("/upload_image", methods=["POST"])
def upload_image():
    image = request.files["image"]

    if _file_is_valid(image.filename):
        storage_client = storage.Client()
        bucket = storage_client.lookup_bucket("mosavid.appspot.com")
        blob = bucket.blob(image.filename)
        blob.upload_from_file(image)

        return "", 204

    return "Invalid video", 400


if __name__ == "__main__":
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    # Flask's development server will automatically serve static files in
    # the "static" directory. See:
    # http://flask.pocoo.org/docs/1.0/quickstart/#static-files. Once deployed,
    # App Engine itself will serve those files as configured in app.yaml.
    app.run(host="127.0.0.1", port=8080, debug=True)
