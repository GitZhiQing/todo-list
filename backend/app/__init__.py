from fastapi import FastAPI

from app.api.routes import router as api_router
from app.core.config import settings
from app.core.lifecycle import lifespan
from app.core.middlewares import register_middleware


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.APP_NAME,
        openapi_url=f"{settings.API_PREFIX}/openapi.json",
        lifespan=lifespan,
        debug=settings.DEBUG,
    )
    register_middleware(app)

    @app.get("/", tags=["root"])
    async def read_root():
        return {
            "name": settings.APP_NAME,
            "environment": settings.APP_ENV,
            "debug": settings.DEBUG,
            "host": settings.HOST,
            "port": settings.PORT,
            "docs": app.docs_url,
        }

    app.include_router(api_router, prefix=settings.API_PREFIX)
    return app


app = create_app()
