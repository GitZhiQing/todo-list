from fastapi import HTTPException
from fastapi.openapi.utils import validation_error_definition, validation_error_response_definition


class BizException(HTTPException):
    """业务错误

    统一覆盖 HTTP Status Code 为 200
    """

    def __init__(self, code: int = 400, msg: str = "业务错误"):
        super().__init__(status_code=200)
        self.code = code
        self.msg = msg


validation_error_response_definition["properties"] = {
    "code": {"type": "integer", "example": 422},
    "msg": {"type": "string", "example": "参数错误"},
    "data": validation_error_definition,
}
