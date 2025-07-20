from fastapi import APIRouter

from app.core.exception import BizException
from app.core.handlers import success
from app.crud import todo_crud
from app.deps import session_dep
from app.schemas import BaseResponse, PageResult, Todo, TodoCreate, TodoUpdate

router = APIRouter()


@router.post("/", response_model=BaseResponse[Todo], status_code=201)
async def create_todo(session: session_dep, todo_in: TodoCreate):
    """创建 Todo 项"""
    todo = await todo_crud.create(session, todo_in=todo_in)
    return success(todo)


@router.get("/", response_model=BaseResponse[PageResult[Todo]])
async def read_todos(
    session: session_dep,
    page: int = 1,
    size: int = 10,
):
    """获取所有 Todo 项"""
    skip = (page - 1) * size
    total = await todo_crud.count(session)
    items = await todo_crud.get_multi(session, skip=skip, limit=size)
    return success(PageResult(total=total, page=page, size=size, items=items))


@router.get("/{todo_id}", response_model=BaseResponse[Todo])
async def read_todo(session: session_dep, todo_id: int):
    """获取指定 Todo 项"""
    todo = await todo_crud.get_or_404(session, todo_id=todo_id)
    return success(todo)


@router.put("/{todo_id}", response_model=BaseResponse[Todo])
async def update_todo(
    session: session_dep,
    todo_id: int,
    todo_in: TodoUpdate,
):
    """更新指定 Todo 项"""
    updated = await todo_crud.update(session, todo_id=todo_id, todo_in=todo_in)
    return success(updated)


@router.delete("/{todo_id}", status_code=204)
async def delete_todo(session: session_dep, todo_id: int):
    """删除指定 Todo 项"""
    deleted = await todo_crud.delete(session, todo_id=todo_id)
    if not deleted:
        raise BizException(code=404, msg="Todo not found")
