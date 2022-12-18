from quart import current_app
from pathlib import Path
from sqlite3 import dbapi2 as sqlite3
from typing import Optional
from quart import Quart, current_app, g
import aiosqlite
from aiosqlite import Connection


async def _connect_db() -> Connection:
    path = current_app.root_path / ".." /"modlog.db"
    print(f"connecting to database at {path}")
    _engine = await aiosqlite.connect(path)
    print("connected to database")
    _engine.row_factory = sqlite3.Row
    with open(current_app.root_path / "config" / "schema.sql", mode="r") as file_:
        await _engine.executescript(file_.read())
    await _engine.commit()
    print("created schema")
    return _engine


class Database:
    def __init__(self, app: Quart) -> None:
        print("preparing database")
        self.app = app
        app.before_serving(self._before_serving)
        app.after_serving(self._after_serving)

    async def _before_serving(self) -> None:
        if not hasattr(self.app, "sqlite_db"):
            print("no database connection yet")
            self.app.sqlite_db = await _connect_db()
            print(f"database connection stored: {self.app.sqlite_db}")

    async def _after_serving(self) -> None:
        await self.app.sqlite_db.close()

