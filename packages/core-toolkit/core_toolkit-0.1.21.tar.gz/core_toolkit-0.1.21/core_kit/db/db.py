import logging
from uuid import uuid4

from asyncpg import Connection  # type:ignore[import-untyped]
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.pool import NullPool

from .settings import settings

logger = logging.getLogger(__name__)


# https://github.com/sqlalchemy/sqlalchemy/issues/6467
class CustomisedAsyncpgConnection(Connection):
    def _get_unique_id(self, prefix: str) -> str:
        return f"__asyncpg_{prefix}_{uuid4()}__"


def async_engine(db_url, app_name, /, use_queue_pool=False, echo=False) -> AsyncEngine:
    pool_params = {"poolclass": NullPool}
    if use_queue_pool:
        pool_params = {
            "pool_size": settings.POOL_SIZE,  # type:ignore[dict-item]
            "max_overflow": settings.MAX_OVERFLOW,  # type:ignore[dict-item]
        }
    engine: AsyncEngine = create_async_engine(
        db_url,
        connect_args={
            "connection_class": CustomisedAsyncpgConnection,
            "prepared_statement_cache_size": settings.PREPARED_STATEMENT_CACHE_SIZE,
            "statement_cache_size": settings.STATEMENT_CACHE_SIZE,
            "server_settings": {
                "application_name": app_name,
                "jit": "off",
            },
        },
        **pool_params,
        echo=echo,
    )
    logger.debug(f"Engine created with params: {pool_params}, {echo=}")
    return engine


def create_async_session_maker(engine):
    session_maker = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    return session_maker
