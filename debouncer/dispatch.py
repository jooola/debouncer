import asyncio

from httpx import Client, Request
from loguru import logger

from .schema import CallStatus, Endpoint
from .store import Store

client = Client()


async def dispatch(store: Store, endpoint: Endpoint):
    endpoint = store.get(endpoint.uid)
    if endpoint.call is None:
        raise ValueError(f"{endpoint.uid}: dispatching endpoint without call")

    # Make endpoint call
    logger.debug(f"{endpoint.uid}: dispatching call")
    request = Request(endpoint.method, endpoint.url)
    response = client.send(request)
    response.raise_for_status()

    endpoint.call.status = CallStatus.DISPATCHED
    store.save(endpoint.uid, endpoint)

    # Wait for eventual timeout endpoint
    logger.info(f"{endpoint.uid}: handling timeout")
    if endpoint.timeout > 0:
        logger.info(f"{endpoint.uid}: waiting {endpoint.timeout} seconds timeout")
        await asyncio.sleep(endpoint.timeout)

    # Close call or redispatch
    endpoint = store.get(endpoint.uid)
    await close_call_or_redispatch(store, endpoint)


async def close_call_or_redispatch(store: Store, endpoint: Endpoint) -> Endpoint:
    if endpoint.call is not None and endpoint.call.redispatch:
        logger.info(f"{endpoint.uid}: redispatching call")
        endpoint.call.redispatch = False
        store.save(endpoint.uid, endpoint)
        await dispatch(store, endpoint)
    else:
        logger.info(f"{endpoint.uid}: closing call")
        endpoint.call = None
        store.save(endpoint.uid, endpoint)

    return endpoint
