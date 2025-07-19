import ujson
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.config import settings

async_engine = create_async_engine(
    url=settings.SQLALCHEMY_DATABASE_URI,
    # 连接池配置
    pool_size=10,  # 核心连接池大小
    max_overflow=20,  # 超出 pool_size 时允许创建的临时连接数
    pool_timeout=30,  # 获取连接等待超时(秒)
    pool_recycle=1800,  # 连接自动回收周期(秒)
    pool_pre_ping=True,  # 执行前自动测试连接有效性
    # 日志与调试
    echo=False,  # 是否输出 SQL 日志
    echo_pool=False,  # 是否记录连接池事件
    # 性能优化
    json_serializer=ujson.dumps,  # ujson 序列化
    json_deserializer=ujson.loads,  # ujson 反序列化
    connect_args={"check_same_thread": False},  # 允许多线程访问
)

async_session_factory = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,  # 提交后不自动过期对象
    autoflush=False,  # 禁用自动 flush
    future=True,  # 显示指定使用 SQLAlchemy 2.0 API
)
