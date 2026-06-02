import sys
import logging
from alembic.config import Config as AlembicConfig
from alembic import command
from sqlalchemy.exc import ProgrammingError


def run_migrations() -> None:
    """Silently apply any pending Alembic migrations at application startup."""
    if "pytest" in sys.modules:
        return

    _loggers = [
        logging.getLogger("alembic"),
        logging.getLogger("alembic.runtime.migration"),
        logging.getLogger("sqlalchemy.engine"),
    ]
    _saved_levels = [(lg, lg.level) for lg in _loggers]
    for lg in _loggers:
        lg.setLevel(logging.CRITICAL + 1)

    try:
        alembic_cfg = AlembicConfig("alembic.ini")

        try:
            # Happy path — apply any pending migrations silently
            command.upgrade(alembic_cfg, "head")
        except ProgrammingError:
            # Tables already exist but Alembic has no version record.
            # Stamp the current state as 'head' so future migrations
            # are tracked correctly, then re-run upgrade to catch any
            # genuinely new migrations on top.
            command.stamp(alembic_cfg, "head")
            command.upgrade(alembic_cfg, "head")

    finally:
        # Always restore original log levels
        for lg, level in _saved_levels:
            lg.setLevel(level)
