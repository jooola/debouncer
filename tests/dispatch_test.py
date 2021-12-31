from datetime import datetime

import pytest

from debouncer.dispatch import dispatch
from debouncer.schema import Endpoint
from debouncer.store import Store


@pytest.mark.asyncio
async def test_dispatch(store: Store, endpoint: Endpoint):
    store.save(endpoint.uid, endpoint)

    start = datetime.now()
    await dispatch(store, endpoint)
    end = datetime.now()

    result = store.get(endpoint.uid)
    assert (end - start).seconds == pytest.approx(2)
    assert result.call is None


@pytest.mark.asyncio
async def test_dispatch_with_redispatch(store: Store, endpoint: Endpoint):
    endpoint.call.redispatch = True
    store.save(endpoint.uid, endpoint)

    start = datetime.now()
    await dispatch(store, endpoint)
    end = datetime.now()

    result = store.get(endpoint.uid)
    assert (end - start).seconds == pytest.approx(4)
    assert result.call is None
