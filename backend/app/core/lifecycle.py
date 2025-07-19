from contextlib import asynccontextmanager

from fastapi import FastAPI
from loguru import logger
from sqlalchemy import text
from tenacity import before_sleep_log, retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from app.core.config import settings
from app.core.database import async_engine


@retry(
    stop=stop_after_attempt(3),  # 最大重试次数
    wait=wait_exponential(multiplier=1, min=1, max=10),  # 指数退避
    retry=retry_if_exception_type(),  # 所有异常都重试
    before_sleep=before_sleep_log(logger, "重试: {wait}s"),  # 重试前日志
)
async def db_connect():
    """数据库连接测试"""
    logger.info("测试数据库连接...")
    async with async_engine.connect() as conn:
        await conn.execute(text("SELECT 1"))
        logger.info("数据库连接成功!")


async def db_init(force_drop: bool = False):
    """数据库初始化

    - force_drop: 是否强制删除重建（生产环境下不允许强制删除）
    """
    from app import models  # noqa: F401
    from app.models import Base

    logger.info("数据库初始化...")
    try:
        async with async_engine.begin() as conn:
            if force_drop:
                logger.info("删除旧表...")
                await conn.run_sync(Base.metadata.drop_all)
                logger.info("已强制删除旧表!")
            await conn.run_sync(Base.metadata.create_all)
            logger.info("数据库初始化完成!")
    except Exception as e:
        logger.error(f"数据库初始化失败: {e}")
        raise


async def db_drop():
    """删除数据库表"""
    from app import models  # noqa: F401
    from app.models import Base

    if settings.APP_ENV == "production":
        raise RuntimeError("生产环境禁止强制删除数据库表")
    logger.info("开始清理数据库...")
    try:
        async with async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            logger.info("数据库清理完成!")
    except Exception as e:
        logger.error(f"数据库清理失败: {e}")
        raise


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    logger.info(
        f"应用 {app.title} 启动...\n"
        f"[+] 环境: {settings.APP_ENV}\n"
        f"[+] 调试: {settings.DEBUG}\n"
        f"[+] 主机: {settings.HOST}\n"
        f"[+] 端口: {settings.PORT}"
    )
    try:
        # 确保 settings.DATA_DIR 存在
        settings.DATA_DIR.mkdir(parents=True, exist_ok=True)
        await db_connect()  # 测试数据库连接
        if settings.APP_ENV != "production":  # 开发和测试环境下强制删除旧表
            await db_init(force_drop=True)
        else:
            await db_init(force_drop=False)
        logger.info("应用启动成功!")
    except Exception as e:
        logger.error(f"应用启动失败: {e}")
        raise e

    yield

    logger.info(f"应用 {app.title} 关闭...")
    try:
        if settings.APP_ENV != "production":
            await db_drop()  # 开发和测试环境下删除数据库表
        await async_engine.dispose()
        logger.info("应用关闭成功!")
    except Exception as e:
        logger.error(f"应用关闭失败: {e}")
        raise
