from typing import List, Optional
from uuid import UUID

from fastapi import (
    APIRouter,
    BackgroundTasks,
    Body,
    Depends,
    HTTPException,
    Query,
    Request,
)
from loguru import logger

from .dispatch import dispatch
from .schema import Call, CallStatus, Endpoint, EndpointCreate


async def verify_auth_key(req: Request, auth: Optional[str] = Query(None)):
    if req.app.config.auth_key is not None and req.app.config.auth_key != auth:
        raise HTTPException(status_code=400, detail="Invalid auth key")


router = APIRouter(
    prefix="/api",
    dependencies=[Depends(verify_auth_key)],
)


@router.get("/", response_model=List[Endpoint], tags=["endpoints"])
async def get_endpoints(req: Request):
    return req.app.store.all()


@router.post("/", response_model=Endpoint, status_code=201, tags=["endpoints"])
async def create_endpoint(
    req: Request,
    body: EndpointCreate = Body(...),
):
    endpoint = Endpoint.from_create(body)
    req.app.store.save(endpoint.uid, endpoint)
    return endpoint


async def endpoint_ctx(
    req: Request,
    uid: UUID,
):
    if uid not in req.app.store:
        raise HTTPException(status_code=404, detail="Endpoint not found")
    return req.app.store.get(uid)


@router.delete("/{uid}", tags=["endpoints"])
async def delete_endpoint(
    req: Request,
    endpoint: Endpoint = Depends(endpoint_ctx),
):
    req.app.store.delete(endpoint.uid)
    return


@router.post("/{uid}", response_model=Call, tags=["calls"])
async def create_call(
    req: Request,
    worker: BackgroundTasks,
    endpoint: Endpoint = Depends(endpoint_ctx),
):
    if endpoint.call is None:
        logger.debug(f"{endpoint.uid}: creating new call")
        endpoint.call = Call()
        req.app.store.save(endpoint.uid, endpoint)
        worker.add_task(dispatch, req.app.store, endpoint)

    # Initial request not yet dispatched, ignoring
    # if endpoint.call.status == CallStatus.CREATED:

    # Initial request dispatched but new requests can be ignored, ignoring
    # if endpoint.call.status == CallStatus.DISPATCHED:

    # Initial request dispatched and locked, new request will be redispatched
    # once the initial request is deleted
    if endpoint.call.status == CallStatus.LOCKED:
        logger.debug(f"{endpoint.uid}: call is locked, it should be redispatched")
        endpoint.call.redispatch = True
        req.app.store.save(endpoint.uid, endpoint)

    return endpoint.call


@router.post("/{uid}/lock", tags=["calls"])
async def lock_call(
    req: Request,
    endpoint: Endpoint = Depends(endpoint_ctx),
):
    if endpoint.call is None:
        raise HTTPException(status_code=404, detail="Call not found")

    logger.debug(f"{endpoint.uid}: locking call")
    endpoint.call.status = CallStatus.LOCKED
    req.app.store.save(endpoint.uid, endpoint)
    return endpoint.call


@router.post("/{uid}/close", tags=["calls"])
async def close_call(
    req: Request,
    endpoint: Endpoint = Depends(endpoint_ctx),
):
    logger.debug(f"{endpoint.uid}: closing call")
    endpoint.call = None
    req.app.store.save(endpoint.uid, endpoint)
    return endpoint.call
