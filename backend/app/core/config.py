from pathlib import Path
from typing import Literal

from dotenv import load_dotenv
from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "Todo List Web API"
    APP_ENV: Literal["development", "testing", "production"] = "development"
    HOST: str = "127.0.0.1"
    PORT: int = 8080
    DEBUG: bool = False if APP_ENV != "production" else True
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


load_dotenv()
settings = Settings()
