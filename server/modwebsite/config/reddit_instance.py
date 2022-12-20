import logging

import asyncpraw
from quart import Quart


class RedditInstance:
    def __init__(self, app: Quart) -> None:
        self.logger = logging.getLogger(__name__)
        self.app = app
        app.before_serving(self._before_serving)
        app.after_serving(self._after_serving)

    async def _before_serving(self) -> None:
        if not hasattr(self.app, "reddit"):
            secrets = {
                'username': self.app.modwebsite_config['reddit']['username'],
                'password': self.app.modwebsite_config['reddit']['password'],
                'client_id': self.app.modwebsite_config['reddit']['client_id'],
                'client_secret': self.app.modwebsite_config['reddit']['client_secret']
            }

            reddit_instance = asyncpraw.Reddit(**secrets,
                             user_agent="com.halfdane.superstonk_mod_website:v0.0.1 (by u/half_dane)")

            self.app.reddit = reddit_instance
            self.logger.info(f"Reddit connection: {await self.app.reddit.user.me()}")

    async def _after_serving(self) -> None:
        await self.app.reddit.close()
