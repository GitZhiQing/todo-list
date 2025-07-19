from pydantic import BaseModel, ConfigDict


class TodoCreate(BaseModel):
    """Todo 创建模型"""

    title: str
    description: str | None = None


class TodoUpdate(BaseModel):
    """Todo 更新模型"""

    title: str | None = None
    description: str | None = None
    completed: bool | None = None


class Todo(BaseModel):
    """Todo 模型

    从数据库中获取的数据映射到该模型
    """

    id: int
    title: str | None = None
    description: str | None = None
    completed: bool | None = None
    created_at: int
    updated_at: int
    model_config = ConfigDict(from_attributes=True)
