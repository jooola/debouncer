from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.responses import FileResponse

from .router import router
from .store import store

static_path = Path(__file__).parent.parent / "web/dist"


def create_app():
    app = FastAPI()
    app.include_router(router)
    app.mount("/assets", StaticFiles(directory=static_path / "assets"), name="assets")

    @app.get("/")
    async def index():
        return FileResponse(static_path / "index.html")

    @app.on_event("shutdown")
    async def shutdown():
        store.close()

    return app
