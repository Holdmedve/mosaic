import os
import pytest
from io import BytesIO
from typing import Any

from main import TEMP_CONTENT_PATH


def test__create_mosaic__send_request__does_not_throw_exception(client: Any) -> None:
    data = {
        "video": (BytesIO(bytes()), "video"),
        "image": (BytesIO(bytes()), "image"),
    }

    client.post("/create_mosaic", data=data)


def test__create_mosaic__saves_video_and_image_from_request(
    client: Any, mocker: Any
) -> None:
    mocker.patch("main.mosavid.create_mosaic_from_video")
    delete_all_files_in_directory(TEMP_CONTENT_PATH)
    data = {
        "video": (BytesIO(bytes()), "video"),
        "image": (BytesIO(bytes()), "image"),
    }

    client.post("/create_mosaic", data=data)

    _, _, files = next(os.walk(TEMP_CONTENT_PATH))
    assert len(files) == 2


def test__root__response_contains_right_input_elements(client: Any) -> None:
    response = client.get("/")

    assert b'<input type="file" id="image_input" name="image">' in response.data
    assert b'<input type="file" id="video_input" name="video">' in response.data


def test__root__response_contains_form_with_right_attributes(client: Any) -> None:
    response = client.get("/")

    assert (
        b'<form method="POST" action="/create_mosaic" enctype="multipart/form-data">'
        in response.data
    )


def test__root__translates_url_for_static_folder(client: Any) -> None:
    response = client.get("/")

    assert b'img src="/static/"' in response.data


def delete_all_files_in_directory(directory_path: str) -> None:
    for path in os.listdir(directory_path):
        full_path = os.path.join(directory_path, path)
        if not os.path.isdir(full_path):
            os.remove(full_path)
