import pytest
from fastapi.testclient import TestClient

from debouncer.app import create_app
from debouncer.config import Config
from debouncer.schema import Call, Endpoint, EndpointCreate
from debouncer.store import Store


@pytest.fixture(name="app")
def fixture_app(tmp_path):
    test_config = Config()
    test_config.store_path = str(tmp_path / "test.db")
    yield create_app(test_config)


@pytest.fixture(name="client")
def fixture_client(app):
    yield TestClient(app)


@pytest.fixture(name="store")
def fixture_store(tmp_path):
    yield Store(tmp_path / "debouncer.db")


@pytest.fixture(name="endpoint")
def fixture_endpoint():
    value = Endpoint.from_create(EndpointCreate(url="http://example.com", timeout=1))
    value.call = Call()
    return value
