import uuid
import cv2

from flask import Flask, render_template, request, send_from_directory, Response
from project import mosavid
from project.types import Config

# from PIL import Image

app = Flask(
    __name__,
    template_folder="project/templates",
    static_folder="project/static",
)

TEMP_CONTENT_PATH = "/tmp"


@app.route("/")
def root() -> str:
    squares = [2**x for x in range(10, 14)]
    return render_template("index.html", tile_count_values=squares)


@app.route("/create_mosaic", methods=["POST"])
def create_mosaic() -> Response:
    image = request.files["image"]
    video = request.files["video"]
    tile_count = int(str(request.form.get("tile_count")))

    image_path = f"{TEMP_CONTENT_PATH}/{uuid.uuid1()}"
    video_path = f"{TEMP_CONTENT_PATH}/{uuid.uuid1()}"
    image.save(image_path)
    video.save(video_path)

    mosaic = mosavid.generate_mosaic(
        config=Config(
            original_image_path=image_path,
            video_path=video_path,
            mosaic_tile_count=tile_count,
            max_frames_to_match=1000,
        )
    )
    mosaic_file_name = f"{uuid.uuid1()}.jpg"
    mosaic_file_path = f"{TEMP_CONTENT_PATH}/{mosaic_file_name}"
    cv2.imwrite(filename=mosaic_file_path, img=mosaic)

    return send_from_directory(directory=TEMP_CONTENT_PATH, path=mosaic_file_name)


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
