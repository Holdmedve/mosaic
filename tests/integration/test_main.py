import pytest
from io import BytesIO


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
        self, app, client, file, expected_status_code
    ):
        app.config["UPLOAD_EXTENSIONS"] = [".jpg", ".mp4"]
        data = {
            "file": (BytesIO(bytes()), file),
        }

        res = client.post("/", data=data)

        assert res.status_code == expected_status_code
