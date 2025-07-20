from fastapi import HTTPException


class BizException(HTTPException):
    """业务错误

    统一覆盖 HTTP Status Code 为 200
    """

    def __init__(self, code: int = 400, msg: str = "业务错误"):
        super().__init__(status_code=200)
        self.code = code
        self.msg = msg
