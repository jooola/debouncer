import uvicorn  # type: ignore

from .app import create_app
from .config import get_config


def run():
    app = create_app(get_config())
    uvicorn.run(app, port=app.config.port)
