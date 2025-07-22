from typing import TypeVar

from pydantic import BaseModel, ConfigDict


class TodoCreate(BaseModel):
    """Todo 创建模型"""

    title: str
    description: str | None = None
    deadline: int | None = None


class TodoUpdate(BaseModel):
    """Todo 更新模型"""

    title: str | None = None
    description: str | None = None
    completed: bool | None = None
    deadline: int | None = None


class Todo(BaseModel):
    """Todo 模型

    从数据库中获取的数据映射到该模型
    """

    id: int
    title: str | None = None
    description: str | None = None
    completed: bool | None = None
    deadline: int | None = None
    created_at: int
    updated_at: int
    model_config = ConfigDict(from_attributes=True)


DataType = TypeVar("DataType")


class BaseResponse[DataType](BaseModel):
    """通用 API 响应模型"""

    code: int = 200
    msg: str = "success"
    data: DataType | None = None


ItemType = TypeVar("ItemType ")


class PageResult[ItemType](BaseModel):
    """分页查询结果模型"""

    total: int  # 总记录数
    page: int  # 当前页码
    size: int  # 每页大小
    items: list[ItemType]  # 当前页数据列表
