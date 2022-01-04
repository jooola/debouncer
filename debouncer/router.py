import secrets
from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, BackgroundTasks, Body, Depends, HTTPException, Query
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from loguru import logger

from .dispatch import close_call_or_redispatch, dispatch
from .schema import Call, CallStatus, Endpoint, EndpointCreate
from .state import State, get_state

http_basic = HTTPBasic(auto_error=False)


async def verify_auth(
    basic_credentials: HTTPBasicCredentials = Depends(http_basic),
    token: Optional[str] = Query(None),
    state: State = Depends(get_state),
):
    if state.config.credentials is None or len(state.config.credentials) == 0:
        return

    username_in = None
    password_in = None

    if basic_credentials is not None:
        username_in = basic_credentials.username
        password_in = basic_credentials.password

    if token is not None:
        token_credentials = token.split(":", maxsplit=1)
        if len(token_credentials) == 2:
            username_in = token_credentials[0]
            password_in = token_credentials[1]

    if not (username_in is None or password_in is None):
        password = state.config.credentials.get(username_in)
        if password is not None and secrets.compare_digest(password_in, password):
            return

    raise HTTPException(
        status_code=401,
        detail="Incorrect credentials",
        headers={"WWW-Authenticate": "Basic"},
    )


router = APIRouter(
    prefix="/api",
    dependencies=[Depends(verify_auth)],
)


@router.get("/", response_model=List[Endpoint], tags=["endpoints"])
async def get_endpoints(state: State = Depends(get_state)):
    return state.store.all()


@router.post("/", response_model=Endpoint, status_code=201, tags=["endpoints"])
async def create_endpoint(
    body: EndpointCreate = Body(...),
    state: State = Depends(get_state),
):
    endpoint = Endpoint.from_create(body)
    state.store.save(endpoint.uid, endpoint)
    return endpoint


async def endpoint_ctx(
    uid: UUID,
    state: State = Depends(get_state),
):
    if uid not in state.store:
        raise HTTPException(status_code=404, detail="Endpoint not found")
    return state.store.get(uid)


@router.delete("/{uid}", tags=["endpoints"])
async def delete_endpoint(
    endpoint: Endpoint = Depends(endpoint_ctx),
    state: State = Depends(get_state),
):
    state.store.delete(endpoint.uid)
    return


@router.post("/{uid}", response_model=Call, tags=["calls"])
async def create_call(
    worker: BackgroundTasks,
    endpoint: Endpoint = Depends(endpoint_ctx),
    state: State = Depends(get_state),
):
    if endpoint.call is None:
        logger.debug(f"{endpoint.uid}: creating new call")
        endpoint.call = Call()
        state.store.save(endpoint.uid, endpoint)
        worker.add_task(dispatch, state.store, endpoint)

    # Initial request not yet dispatched, ignoring
    # if endpoint.call.status == CallStatus.CREATED:

    # Initial request dispatched but new requests can be ignored, ignoring
    # if endpoint.call.status == CallStatus.DISPATCHED:

    # Initial request dispatched and locked, new request will be redispatched
    # once the initial request is deleted
    if endpoint.call.status == CallStatus.LOCKED:
        logger.debug(f"{endpoint.uid}: call is locked, it should be redispatched")
        endpoint.call.redispatch = True
        state.store.save(endpoint.uid, endpoint)

    return endpoint.call


@router.post("/{uid}/lock", tags=["calls"])
async def lock_call(
    endpoint: Endpoint = Depends(endpoint_ctx),
    state: State = Depends(get_state),
):
    if endpoint.call is None:
        raise HTTPException(status_code=404, detail="Call not found")

    logger.debug(f"{endpoint.uid}: locking call")
    endpoint.call.status = CallStatus.LOCKED
    state.store.save(endpoint.uid, endpoint)
    return endpoint.call


@router.post("/{uid}/close", tags=["calls"])
async def close_call(
    endpoint: Endpoint = Depends(endpoint_ctx),
    state: State = Depends(get_state),
):
    endpoint = await close_call_or_redispatch(state.store, endpoint)
    return endpoint.call
