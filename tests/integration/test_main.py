import pytest
import base64


from io import BytesIO
from google.cloud import storage


SMALLEST_JPEG_B64 = """\
/9j/2wBDAAMCAgICAgMCAgIDAwMDBAYEBAQEBAgGBgUGCQgKCgkICQkKDA8MCgsOCwkJDRENDg8Q
EBEQCgwSExIQEw8QEBD/yQALCAABAAEBAREA/8wABgAQEAX/2gAIAQEAAD8A0s8g/9k=
"""


# class TestUpload:
#     def test__upload_image__image_stored_in_bucket(
#         self, client, mock_file_check, random_file_name
#     ):
#         data = {
#             "image": (BytesIO(base64.b64decode(SMALLEST_JPEG_B64)), random_file_name),
#         }

#         client.post("/upload_image", data=data)

#         blob_iterator = storage.Client().list_blobs("mosavid.appspot.com")
#         blobs = [blob.name for blob in blob_iterator]

#         assert random_file_name in blobs
