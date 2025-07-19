from fastapi import APIRouter, HTTPException

from app import schemas
from app.crud import todo_crud
from app.deps import session_dep

router = APIRouter()


@router.post("/", response_model=schemas.Todo, status_code=201)
async def create_todo(session: session_dep, todo_in: schemas.TodoCreate):
    return await todo_crud.create(session, todo_in=todo_in)


@router.get("/", response_model=list[schemas.Todo])
async def read_todos(
    session: session_dep,
    skip: int = 0,
    limit: int = 100,
):
    return await todo_crud.get_multi(session, skip=skip, limit=limit)


@router.get("/{todo_id}", response_model=schemas.Todo)
async def read_todo(session: session_dep, todo_id: int):
    todo = await todo_crud.get(session, todo_id=todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo


@router.put("/{todo_id}", response_model=schemas.Todo)
async def update_todo(
    session: session_dep,
    todo_id: int,
    todo_in: schemas.TodoUpdate,
):
    updated = await todo_crud.update(session, todo_id=todo_id, todo_in=todo_in)
    if not updated:
        raise HTTPException(status_code=404, detail="Todo not found")
    return updated


@router.delete("/{todo_id}", status_code=204)
async def delete_todo(
    session: session_dep,
    todo_id: int,
):
    deleted = await todo_crud.delete(session, todo_id=todo_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Todo not found")
