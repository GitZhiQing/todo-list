from functools import lru_cache
from pathlib import Path
from typing import Literal

from dotenv import load_dotenv
from loguru import logger
from pydantic import ValidationError, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "Todo List Web API"
    APP_ENV: Literal["development", "testing", "production"] = "development"
    HOST: str = "127.0.0.1"
    PORT: int = 8080
    DEBUG: bool = True if APP_ENV != "development" else False  # 开发模式下启动调试
    API_PREFIX: str = "/api"
    SECRET_KEY: str  # !必须提供
    WORKERS: int = 1 if APP_ENV != "production" else 4

    # 允许的主机列表
    @computed_field
    @property
    def ALLOWED_HOSTS(self) -> list[str]:
        return list({self.HOST, "localhost", "127.0.0.1"})

    # 文件路径配置
    APP_DIR: Path = Path(__file__).resolve().parent.parent
    DATA_DIR: Path = APP_DIR.parent / "data"
    SQLITE_DB_PATH: Path = DATA_DIR / "db.sqlite3"

    # 数据库配置
    SQLALCHEMY_DATABASE_URI: str = f"sqlite+aiosqlite:///{SQLITE_DB_PATH}"

    # 前端 URL (用于 CORS 设置)
    FRONTEND_URL: str = "http://localhost:5173"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=True,
    )


@lru_cache
def get_settings() -> Settings:
    try:
        load_dotenv()
        return Settings()
    except ValidationError as e:
        logger.error(f"配置导入错误: {e}")
        required = {name: field.annotation for name, field in Settings.model_fields.items() if field.is_required()}
        if required:
            logger.error(f"[!] 缺少必需环境变量 [{', '.join(required)}]，请创建 .env 文件并在其中配置")
        exit(1)
