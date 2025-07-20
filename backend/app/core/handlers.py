from typing import Any

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from loguru import logger
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.core.exception import BizException
from app.schemas import BaseResponse


def success(data: Any = None, msg: str = "success") -> BaseResponse:
    return BaseResponse(code=200, msg=msg, data=data)


def failed(code: int = 400, msg: str = "failed", data: Any = None) -> BaseResponse:
    return BaseResponse(code=code, msg=msg, data=data)


def register_handlers(app: FastAPI):
    @app.exception_handler(BizException)
    async def biz_exception_handler(
        request: Request,  # noqa: ARG001
        exc: BizException,
    ):
        return JSONResponse(status_code=200, content=failed(code=exc.code, msg=exc.msg).model_dump())

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        request: Request,  # noqa: ARG001
        exc: RequestValidationError,
    ):
        return JSONResponse(status_code=200, content=failed(code=422, msg="参数错误", data=exc.errors()).model_dump())

    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(
        request: Request,  # noqa: ARG001
        exc: StarletteHTTPException,
    ):
        return JSONResponse(status_code=200, content=failed(code=exc.status_code, msg=exc.detail).model_dump())

    @app.exception_handler(Exception)
    async def all_exception_handler(
        request: Request,  # noqa: ARG001
        exc: Exception,
    ):
        logger.error(f"服务器内部错误: {exc}")
        return JSONResponse(status_code=200, content=failed(code=500, msg="服务器内部错误").model_dump())
