import logging
from sqlite3 import dbapi2 as sqlite3

import aiosqlite
from aiosqlite import Connection
from quart import Quart, current_app

logger = logging.getLogger(__name__)


async def _connect_db() -> Connection:
    path = current_app.root_path / ".." /"modlog.db"
    logger.debug(f"connecting to database at {path}")
    _engine = await aiosqlite.connect(path)
    logger.debug("connected to database")
    _engine.row_factory = sqlite3.Row
    with open(current_app.root_path / "config" / "schema.sql", mode="r") as file_:
        await _engine.executescript(file_.read())
    await _engine.commit()
    logger.debug("created schema")
    return _engine


def database(app: Quart):
    logger.debug("preparing database")

    @app.before_serving
    async def _before_serving() -> None:
        if not hasattr(app, "sqlite_db"):
            logger.debug("no database connection yet")
            app.sqlite_db = await _connect_db()
            logger.debug(f"database connection stored: {app.sqlite_db}")

    @app.after_serving
    async def _after_serving() -> None:
        await app.sqlite_db.close()
