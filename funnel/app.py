from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from starlette.responses import FileResponse

from .router import router
from .store import store


def create_app():
    app = FastAPI()
    app.include_router(router)
    app.mount("/assets", StaticFiles(directory="web/dist/assets"), name="assets")

    @app.get("/")
    async def index():
        return FileResponse("web/dist/index.html")

    @app.on_event("shutdown")
    async def shutdown():
        store.close()

    return app
