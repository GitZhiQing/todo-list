from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Todo
from app.schemas import TodoCreate, TodoUpdate


class TodoCRUD:
    async def create(self, session: AsyncSession, *, todo_in: TodoCreate) -> Todo:
        db_todo = Todo(**todo_in.model_dump(exclude_unset=True))
        session.add(db_todo)
        await session.flush()
        await session.refresh(db_todo)
        return db_todo

    async def get(self, session: AsyncSession, *, todo_id: int) -> Todo | None:
        stmt = select(Todo).where(Todo.id == todo_id)
        result = await session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_multi(self, session: AsyncSession, *, skip: int = 0, limit: int = 100) -> list[Todo]:
        stmt = select(Todo).offset(skip).limit(limit)
        result = await session.execute(stmt)
        return result.scalars().all()

    async def update(self, session: AsyncSession, *, todo_id: int, todo_in: TodoUpdate) -> Todo | None:
        db_todo = await self.get(session, todo_id=todo_id)
        if not db_todo:
            return None
        update_data = todo_in.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_todo, key, value)
        await session.flush()
        return db_todo

    async def delete(self, session: AsyncSession, *, todo_id: int) -> bool:
        db_todo = await self.get(session, todo_id=todo_id)
        if not db_todo:
            return False
        await session.delete(db_todo)
        await session.flush()
        return True


todo_crud = TodoCRUD()
