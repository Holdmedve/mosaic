import pytest

from main import app as flask_app


@pytest.fixture
def app():
    yield flask_app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def mock_storage(mocker):
    return mocker.patch("main.storage")


@pytest.fixture
def mock_file_check(mocker):
    return mocker.patch("main._file_is_valid", return_value=True)
