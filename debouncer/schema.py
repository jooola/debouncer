from enum import Enum
from typing import Optional
from uuid import UUID, uuid5

from pydantic import BaseModel, HttpUrl

UUID_NAMESPACE = UUID("dabdee1d-f505-4b7c-8447-6b32df38eb77")


class CallStatus(str, Enum):
    CREATED = "created"
    DISPATCHED = "dispatched"
    LOCKED = "locked"


class Call(BaseModel):
    status: CallStatus = CallStatus.CREATED
    redispatch: bool = False


class EndpointMethod(str, Enum):
    POST = "POST"
    GET = "GET"


class BaseEndpoint(BaseModel):
    url: HttpUrl
    method: EndpointMethod = EndpointMethod.POST
    timeout: int = 30


class EndpointCreate(BaseEndpoint):
    pass


class Endpoint(BaseEndpoint):
    uid: UUID
    call: Optional[Call]

    @staticmethod
    def from_create(payload: EndpointCreate) -> "Endpoint":
        return Endpoint(uid=uuid5(UUID_NAMESPACE, payload.url), **dict(payload))
