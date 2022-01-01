from fastapi import Request

from .config import Config
from .store import Store


# pylint: disable=too-few-public-methods
class State:
    config: Config
    store: Store


def get_state(req: Request) -> State:
    return req.app.state
