import pytest
from io import BytesIO


class TestRoot:
    def test__when_called__respones_ok(self, client):
        res = client.get("/")
        assert res.status_code == 200

    def test__get_root__result_contains_target_image_submit_form(self, client):
        res = client.get("/")
        assert (
            b'<form method="POST" action="/upload_image" enctype="multipart/form-data">'
            in res.data
        )
        assert b'<label for="image">Select a target image:</label>' in res.data
        assert (
            b'<input type="file" id="image" name="image" onchange="form.submit()">'
            in res.data
        )

    def test__get_root__result_contains_video_submit_form(self, client):
        res = client.get("/")
        assert (
            b'<form method="POST" action="/upload_video" enctype="multipart/form-data">'
            in res.data
        )
        assert b'<label for="video">Select a video:</label>' in res.data
        assert (
            b'<input type="file" id="video" name="video" onchange="form.submit()">'
            in res.data
        )


class TestUpload:
    def test__upload_video__response_ok(self, client):
        data = {
            "video": (BytesIO(bytes()), "my_video.mp4"),
        }
        res = client.post("/upload_video", data=data)
        assert res.status_code == 204

    def test__upload_image__response_ok(self, client):
        data = {
            "image": (BytesIO(bytes()), "my_image.jpg"),
        }
        res = client.post("/upload_image", data=data)
        assert res.status_code == 204

    @pytest.mark.parametrize(
        "image, expected_status_code",
        [
            ("test_image.jpg", 204),
            ("clearly_malicious_content.exe", 400),
            ("", 400),
        ],
    )
    def test__when_uploading_image__only_accepts_expected_type(
        self, app, client, image, expected_status_code, mock_storage
    ):
        app.config["UPLOAD_EXTENSIONS"] = [".jpg"]
        data = {
            "image": (BytesIO(bytes()), image),
        }

        res = client.post("/upload_image", data=data)

        assert res.status_code == expected_status_code

    @pytest.mark.parametrize(
        "video, expected_status_code",
        [
            ("test_video.mp4", 204),
            ("clearly_malicious_content.exe", 400),
            ("", 400),
        ],
    )
    def test__when_uploading_video__only_accepts_expected_type(
        self, app, client, video, expected_status_code, mock_storage
    ):
        app.config["UPLOAD_EXTENSIONS"] = [".mp4"]
        data = {
            "video": (BytesIO(bytes()), video),
        }

        res = client.post("/upload_video", data=data)

        assert res.status_code == expected_status_code
