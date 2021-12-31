import pytest
from fastapi.testclient import TestClient

from debouncer.app import create_app
from debouncer.config import Config
from debouncer.schema import Call, Endpoint, EndpointCreate
from debouncer.store import Store


@pytest.fixture(name="config")
def fixture_config(tmp_path):
    config = Config()
    config.store_path = str(tmp_path / "test.db")
    return config


@pytest.fixture(name="app")
def fixture_app(config):
    yield create_app(config)


@pytest.fixture(name="app_secure")
def fixture_app_secure(config):
    config.auth_key = "secret"
    yield create_app(config)


@pytest.fixture(name="client")
def fixture_client(app):
    yield TestClient(app)


@pytest.fixture(name="client_secure")
def fixture_client_secure(app_secure):
    yield TestClient(app_secure)


@pytest.fixture(name="store")
def fixture_store(tmp_path):
    yield Store(tmp_path / "debouncer.db")


@pytest.fixture(name="endpoint")
def fixture_endpoint():
    value = Endpoint.from_create(EndpointCreate(url="http://example.com", timeout=1))
    value.call = Call()
    return value
