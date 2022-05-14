import pytest
import random
from main import app as flask_app
from typing import Any


@pytest.fixture
def app() -> Any:
    yield flask_app


@pytest.fixture
def client(app: Any) -> Any:
    return app.test_client()


@pytest.fixture
def random_file_name() -> str:
    randint = random.randint(10000, 100000)
    file_name = f"test-{randint}"
    return file_name
