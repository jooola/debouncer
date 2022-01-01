from fastapi import Request
from pydantic import BaseModel

from .config import Config
from .store import Store


class State(BaseModel):
    config: Config
    store: Store


def get_state(req: Request) -> State:
    return req.app.state
