from typing import List
from uuid import UUID

from fastapi import APIRouter, BackgroundTasks, Body, Depends, HTTPException
from loguru import logger

from .dispatch import dispatch
from .schema import Call, CallStatus, Endpoint, EndpointCreate
from .store import store

router = APIRouter(prefix="/api")


@router.get("/", response_model=List[Endpoint], tags=["endpoints"])
async def get_endpoints():
    return store.all()


@router.post("/", response_model=Endpoint, status_code=201, tags=["endpoints"])
async def create_endpoint(body: EndpointCreate = Body(...)):
    endpoint = Endpoint.from_create(body)
    store.save(endpoint.uid, endpoint)
    return endpoint


async def endpoint_ctx(uid: UUID):
    if uid not in store:
        raise HTTPException(status_code=404, detail="Endpoint not found")
    return store.get(uid)


@router.delete("/{uid}", tags=["endpoints"])
async def delete_endpoint(endpoint: Endpoint = Depends(endpoint_ctx)):
    store.delete(endpoint.uid)
    return


@router.post("/{uid}", response_model=Call, tags=["calls"])
async def create_call(
    worker: BackgroundTasks,
    endpoint: Endpoint = Depends(endpoint_ctx),
):
    if endpoint.call is None:
        logger.debug(f"{endpoint.uid}: creating new call")
        endpoint.call = Call()
        store.save(endpoint.uid, endpoint)
        worker.add_task(dispatch, store, endpoint)

    # Initial request not yet dispatched, ignoring
    # if endpoint.call.status == CallStatus.CREATED:

    # Initial request dispatched but new requests can be ignored, ignoring
    # if endpoint.call.status == CallStatus.DISPATCHED:

    # Initial request dispatched and locked, new request will be redispatched
    # once the initial request is deleted
    if endpoint.call.status == CallStatus.LOCKED:
        logger.debug(f"{endpoint.uid}: call is locked, it should be redispatched")
        endpoint.call.redispatch = True
        store.save(endpoint.uid, endpoint)

    return endpoint.call


@router.post("/{uid}/lock", tags=["calls"])
async def lock_call(endpoint: Endpoint = Depends(endpoint_ctx)):
    if endpoint.call is None:
        raise HTTPException(status_code=404, detail="Call not found")

    logger.debug(f"{endpoint.uid}: locking call")
    endpoint.call.status = CallStatus.LOCKED
    store.save(endpoint.uid, endpoint)
    return endpoint.call


@router.post("/{uid}/close", tags=["calls"])
async def close_call(endpoint: Endpoint = Depends(endpoint_ctx)):
    logger.debug(f"{endpoint.uid}: closing call")
    endpoint.call = None
    store.save(endpoint.uid, endpoint)
    return endpoint.call
