from fastapi import APIRouter, Path
from fastapi.params import Query

from app.core.exception import BizException
from app.core.handlers import success
from app.crud import todo_crud
from app.deps import session_dep
from app.schemas import BaseResponse, PageResult, Todo, TodoCreate, TodoUpdate

router = APIRouter()


@router.post(
    "/",
    response_model=BaseResponse[Todo],
    summary="创建新的 Todo 项",
    description="创建一个新的 Todo 任务并返回创建结果",
)
async def create_todo(session: session_dep, todo_in: TodoCreate):
    """
    创建新的 Todo 项

    - **session**: 数据库会话（自动注入）
    - **todo_in**: Todo 创建数据模型
    """
    todo = await todo_crud.create(session, todo_in=todo_in)
    return success(code=201, data=todo)


@router.get(
    "/{todo_id}",
    response_model=BaseResponse[Todo],
    summary="获取单个 Todo 项",
    description="根据 ID 获取指定的 Todo 任务",
)
async def read_todo(
    session: session_dep,
    todo_id: int = Path(
        ...,
        title="Todo ID",
        description="要查询的 Todo 项ID",
        example=1,
    ),
):
    """
    获取指定 ID 的 Todo 项

    - **session**: 数据库会话（自动注入）
    - **todo_id**: 要查询的 Todo ID
    """
    todo = await todo_crud.get_or_404(session, todo_id=todo_id)
    return success(todo)


@router.get(
    "/",
    response_model=BaseResponse[PageResult[Todo]],
    summary="获取分页的 Todo 列表",
    description="获取分页的 Todo 任务列表，支持页码和每页大小参数",
)
async def read_todos(
    session: session_dep,
    page: int = Query(1, ge=1, title="页码", description="要查询的页码（从1开始）", example=1),
    size: int = Query(10, ge=1, le=100, title="每页大小", description="每页返回的记录数（1-100）", example=10),
):
    """
    获取分页的 Todo 列表

    - **session**: 数据库会话（自动注入）
    - **page**: 当前页码（默认1）
    - **size**: 每页记录数（默认10，最大100）
    """
    skip = (page - 1) * size
    total = await todo_crud.count(session)
    items = await todo_crud.get_multi(session, skip=skip, limit=size)
    return success(PageResult(total=total, page=page, size=size, items=items))


@router.put(
    "/{todo_id}",
    response_model=BaseResponse[Todo],
    summary="更新 Todo 项",
    description="更新指定 ID 的 Todo 任务",
)
async def update_todo(
    session: session_dep,
    todo_in: TodoUpdate,
    todo_id: int = Path(..., title="Todo ID", description="要更新的 Todo 项ID", example=1),
):
    """
    更新指定的 Todo 项

    - **session**: 数据库会话（自动注入）
    - **todo_id**: 要更新的 Todo ID
    - **todo_in**: Todo 更新数据模型
    """
    updated = await todo_crud.update(session, todo_id=todo_id, todo_in=todo_in)
    return success(updated)


@router.delete(
    "/{todo_id}",
    summary="删除 Todo 项",
    description="删除指定 ID 的 Todo 任务",
)
async def delete_todo(
    session: session_dep,
    todo_id: int = Path(
        ...,
        title="Todo ID",
        description="要删除的 Todo 项ID",
        example=1,
    ),
):
    """
    删除指定的 Todo 项

    - **session**: 数据库会话（自动注入）
    - **todo_id**: 要删除的 Todo ID

    成功时返回 code=204（无内容），失败时返回 code=404 错误
    """
    deleted = await todo_crud.delete(session, todo_id=todo_id)
    if not deleted:
        raise BizException(code=404, msg="Todo not found")
    return success(code=204)
