from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.responses import FileResponse

from .config import Config
from .router import router
from .store import get_store

static_path = Path(__file__).parent.parent / "web/dist"


def create_app(config: Config):
    app = FastAPI(
        title="Debouncer",
        description="A proxy that debounce requests.",
        version="0.1.0",
    )

    app.state.config = config
    app.state.store = get_store(config.store_path)

    app.include_router(router)
    app.mount("/assets", StaticFiles(directory=static_path / "assets"), name="assets")

    @app.get("/")
    async def index():
        return FileResponse(static_path / "index.html")

    @app.on_event("shutdown")
    async def shutdown():
        app.state.store.close()

    return app
