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
