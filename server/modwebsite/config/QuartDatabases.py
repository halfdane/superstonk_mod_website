from typing import Any, Optional

from databases import Database
from quart import Quart, current_app


class QuartDatabases:
    def __init__(self, app: Optional[Quart] = None, **db_args: Any) -> None:
        self._db_args = db_args
        if app is not None:
            self.init_app(app)

    def init_app(self, app: Quart) -> None:
        self._url = app.modwebsite_config['database']['connection_url']
        app.before_serving(self._before_serving)
        app.after_serving(self._after_serving)

    async def _before_serving(self) -> None:
        self._db = Database(url=self._url, **self._db_args)
        await self._db.connect()
        current_app.db = self

    async def _after_serving(self) -> None:
        await self._db.disconnect()

    def __getattr__(self, name: str) -> Any:
        return getattr(self._db, name)
