from unittest.mock import patch

import pytest

from debouncer.dispatch import dispatch
from debouncer.schema import Endpoint
from debouncer.store import Store


async def helper_dispatch(store, endpoint, call_count):
    store.save(endpoint.uid, endpoint)

    with patch("debouncer.dispatch.client.send") as mock_client:
        await dispatch(store, endpoint)
        assert mock_client.call_count == call_count

    result = store.get(endpoint.uid)
    assert result.call is None


@pytest.mark.asyncio
async def test_dispatch(store: Store, endpoint: Endpoint):
    await helper_dispatch(store, endpoint, 1)


@pytest.mark.asyncio
async def test_dispatch_with_redispatch(store: Store, endpoint: Endpoint):
    endpoint.call.redispatch = True
    await helper_dispatch(store, endpoint, 2)
