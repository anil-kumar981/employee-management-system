import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase
from app.core.config import Config
from contextlib import asynccontextmanager
import sys
from sqlalchemy import select
from sqlalchemy.pool import NullPool


class Base(DeclarativeBase):
    """Base class for all SQLAlchemy 2.0 models, utilizing DeclarativeBase."""

    pass


# Create a modern asynchronous PostgreSQL database engine
# We use NullPool here because Flask runs in a thread-per-request environment.
# This prevents connections in the pool from getting bound to closed request-scoped event loops.
async_engine = create_async_engine(
    Config.DATABASE_URL, echo=False, future=True, poolclass=NullPool
)


# Async session factory for spawning AsyncSession instances
AsyncSessionLocal = async_sessionmaker(
    bind=async_engine, class_=AsyncSession, expire_on_commit=False
)


@asynccontextmanager
async def get_db():
    """
    Asynchronous context manager yielding a scoped AsyncSession connection.
    Automatically opens a connection and guarantees it is safely closed
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


def init_db(app=None) -> None:
    """Synchronous startup wrapper that verifies database connectivity."""

    # Bypass active PostgreSQL connection setup during unit testing
    if (app and app.config.get("TESTING")) or "pytest" in sys.modules:
        return

    async def _init_database():
        # Schema is fully managed by Alembic migrations (run_migrations in create_app).
        # This only verifies DB connectivity with a lightweight SELECT 1 health check.
        async with async_engine.connect() as conn:
            await conn.execute(select(1))

    try:
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            loop = None

        if loop and loop.is_running():
            # If the event loop is already running, schedule the database init task
            loop.create_task(_init_database())
        else:
            # Run database init on a temporary event loop and dispose engine connections cleanly
            async def _run_and_dispose():
                await _init_database()
                await async_engine.dispose()

            asyncio.run(_run_and_dispose())
    except Exception as e:
        import logging

        logging.getLogger(__name__).error(
            f"Failed to connect to the database during startup: {str(e)}"
        )
        # Raise so that server startup fails visibly if DB credentials are wrong
        raise e
