from time import time

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class TimestampMixin:
    # 秒级时间戳
    created_at: Mapped[int] = mapped_column(default=lambda: int(time()))
    updated_at: Mapped[int] = mapped_column(default=lambda: int(time()), onupdate=lambda: int(time()))


class Todo(Base, TimestampMixin):
    __tablename__ = "todos"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str | None] = mapped_column(nullable=True)
    completed: Mapped[bool] = mapped_column(default=False)

    def __repr__(self) -> str:
        return f"<Todo(id={self.id}, title={self.title}, completed={self.completed})>"
