import uvicorn  # type: ignore

from .app import create_app
from .config import config


def run():
    app = create_app()
    uvicorn.run(app, port=config.port)
