import logging
import typing
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
)

from .db import async_engine, create_async_session_maker

logger = logging.getLogger(__name__)

DB_SESSION_MAKER: typing.Callable
ENGINE: AsyncEngine


def init_db(db_url, app_name, /, use_queue_pool=False, echo=False):
    global DB_SESSION_MAKER
    global ENGINE
    ENGINE = async_engine(db_url, app_name, use_queue_pool, echo)
    DB_SESSION_MAKER = create_async_session_maker(ENGINE)


@asynccontextmanager
async def begin_async_session() -> AsyncGenerator[AsyncSession, None]:
    global DB_SESSION_MAKER
    async with DB_SESSION_MAKER() as session:
        async with session.begin():
            try:
                yield session
            except Exception as e:
                logger.warning(f"Rolling back transaction (due exception={e})")
                raise e


@asynccontextmanager
async def async_session() -> AsyncGenerator[AsyncSession, None]:
    global DB_SESSION_MAKER
    async with DB_SESSION_MAKER() as session:
        yield session
