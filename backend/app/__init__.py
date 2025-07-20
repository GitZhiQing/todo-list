from fastapi import FastAPI
from fastapi.openapi.utils import validation_error_response_definition

from app.api.routes import router as api_router
from app.core.config import settings
from app.core.handlers import register_handlers
from app.core.lifecycle import lifespan
from app.core.middlewares import register_middlewares


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.APP_NAME,
        openapi_url=f"{settings.API_PREFIX}/openapi.json",
        lifespan=lifespan,
        debug=settings.DEBUG,
        # 覆盖参数验证错误的响应定义(保证 API 文档正确)
        validation_error_response_definition=validation_error_response_definition,
    )
    register_middlewares(app)  # 注册中间件
    register_handlers(app)  # 注册异常处理器

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
