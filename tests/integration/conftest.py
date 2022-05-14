import pytest
import random
from main import app as flask_app


@pytest.fixture
def app():
    yield flask_app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def mock_file_check(mocker):
    return mocker.patch("main._file_is_valid", return_value=True)


@pytest.fixture
def random_file_name():
    randint = random.randint(10000, 100000)
    file_name = f"test-{randint}"
    return file_name
