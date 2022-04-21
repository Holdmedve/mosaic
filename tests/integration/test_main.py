import pytest
import base64


from io import BytesIO
from google.cloud import storage


SMALLEST_JPEG_B64 = """\
/9j/2wBDAAMCAgICAgMCAgIDAwMDBAYEBAQEBAgGBgUGCQgKCgkICQkKDA8MCgsOCwkJDRENDg8Q
EBEQCgwSExIQEw8QEBD/yQALCAABAAEBAREA/8wABgAQEAX/2gAIAQEAAD8A0s8g/9k=
"""


class TestMain:
    def test__when_called__returns_200(self, client):
        res = client.get("/")
        assert res.status_code == 200

    def test__when_called__result_contains_droparea_class(self, client):
        res = client.get("/")
        assert b'class="dropzone"' in res.data

    @pytest.mark.parametrize(
        "file, expected_status_code",
        [
            ("test_image.jpg", 204),
            ("test_video.mp4", 204),
            ("clearly_malicious_content.exe", 400),
            ("", 400),
        ],
    )
    def test__when_uploading_file__only_accepts_expected_type(
        self, app, client, file, expected_status_code, mock_storage
    ):
        app.config["UPLOAD_EXTENSIONS"] = [".jpg", ".mp4"]
        data = {
            "file": (BytesIO(bytes()), file),
        }

        res = client.post("/", data=data)

        assert res.status_code == expected_status_code

    def test__upload_file__file_stored_in_bucket(
        self, client, mock_file_check, random_file_name
    ):
        data = {
            "file": (BytesIO(base64.b64decode(SMALLEST_JPEG_B64)), random_file_name),
        }

        client.post("/", data=data)

        blob_iterator = storage.Client().list_blobs("mosavid.appspot.com")
        blobs = [blob.name for blob in blob_iterator]

        assert random_file_name in blobs
