from fastapi import APIRouter

from app.api.routes import todos

router = APIRouter()
router.include_router(todos.router, prefix="/todos", tags=["Todos"])
