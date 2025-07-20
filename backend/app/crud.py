from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exception import BizException
from app.models import Todo
from app.schemas import TodoCreate, TodoUpdate


class TodoCRUD:
    """提供 Todo 实体的 CRUD 操作

    封装所有数据库操作，包括创建、读取、更新和删除 Todo 项
    """

    async def create(self, session: AsyncSession, *, todo_in: TodoCreate) -> Todo:
        """创建新的 Todo 项

        Args:
            session: 异步数据库会话
            todo_in: 包含创建数据的 TodoCreate 对象

        Returns:
            新创建的 Todo 对象（包含数据库生成的ID等字段）
        """
        db_todo = Todo(**todo_in.model_dump(exclude_unset=True))
        session.add(db_todo)
        await session.flush()
        await session.refresh(db_todo)
        return db_todo

    async def get(self, session: AsyncSession, *, todo_id: int) -> Todo | None:
        """根据 ID 获取单个 Todo 项

        Args:
            session: 异步数据库会话
            todo_id: 要获取的 Todo ID

        Returns:
            找到的 Todo 对象，如果不存在则返回 None
        """
        stmt = select(Todo).where(Todo.id == todo_id)
        result = await session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_or_404(self, session: AsyncSession, *, todo_id: int) -> Todo:
        """获取单个 Todo 项，不存在时抛出 404 异常

        Args:
            session: 异步数据库会话
            todo_id: 要获取的 Todo ID

        Returns:
            找到的 Todo 对象

        Raises:
            BizException: 当 Todo 不存在时抛出 code=404 的异常
        """
        todo = await self.get(session, todo_id=todo_id)
        if not todo:
            raise BizException(code=404, msg="Todo not found")
        return todo

    async def get_multi(self, session: AsyncSession, *, skip: int = 0, limit: int = 100) -> list[Todo]:
        """获取多个 Todo 项（分页查询）

        Args:
            session: 异步数据库会话
            skip: 跳过的记录数（用于分页）
            limit: 返回的最大记录数

        Returns:
            Todo 对象列表
        """
        stmt = select(Todo).offset(skip).limit(limit)
        result = await session.execute(stmt)
        return result.scalars().all()

    async def update(self, session: AsyncSession, *, todo_id: int, todo_in: TodoUpdate) -> Todo:
        """更新指定的 Todo 项

        Args:
            session: 异步数据库会话
            todo_id: 要更新的 Todo ID
            todo_in: 包含更新数据的 TodoUpdate 对象

        Returns:
            更新后的 Todo 对象

        Raises:
            BizException: 当 Todo 不存在时抛出 code=404 的异常
        """
        db_todo = await self.get_or_404(session, todo_id=todo_id)
        update_data = todo_in.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_todo, key, value)
        await session.flush()
        return db_todo

    async def delete(self, session: AsyncSession, *, todo_id: int) -> bool:
        """删除指定的 Todo 项

        Args:
            session: 异步数据库会话
            todo_id: 要删除的 Todo ID

        Returns:
            bool: 删除操作是否成功执行（True: 成功删除, False: 记录不存在）
        """
        db_todo = await self.get(session, todo_id=todo_id)
        if not db_todo:
            return False
        await session.delete(db_todo)
        await session.flush()
        return True

    async def count(self, session: AsyncSession) -> int:
        """统计 Todo 总数

        Args:
            session: 异步数据库会话

        Returns:
            数据库中的 Todo 总数
        """
        return await session.scalar(select(func.count(Todo.id)))


# 创建 TodoCRUD 实例供全局使用
todo_crud = TodoCRUD()
