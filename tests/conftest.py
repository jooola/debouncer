import pytest

from funnel.schema import Call, Endpoint, EndpointCreate
from funnel.store import Store


@pytest.fixture(autouse=True)
def store(tmp_path):
    yield Store(tmp_path / "funnel.db")


@pytest.fixture
def endpoint():
    value = Endpoint.from_create(EndpointCreate(url="http://example.com", timeout=2))
    value.call = Call()
    return value
