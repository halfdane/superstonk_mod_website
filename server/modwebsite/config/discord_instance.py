import asyncio
import logging

import disnake
from quart import Quart


class DiscordInstance:
    def __init__(self, app: Quart) -> None:
        self.logger = logging.getLogger(__name__)
        self.app = app
        app.before_serving(self._before_serving)
        app.after_serving(self._after_serving)

    async def _before_serving(self) -> None:
        if not hasattr(self.app, "discord_client"):
            intents = disnake.Intents.default()
            intents.message_content = True
            intents.members = True

            client = disnake.Client()

            loop = asyncio.get_event_loop()
            await client.login(self.app.modwebsite_config['discord']['discord_bot_token'])
            loop.create_task(client.connect())

            self.app.discord_client = client
            self.logger.info(f"Reddit connection: {await self.app.reddit.user.me()}")

    async def _after_serving(self) -> None:
        await self.app.reddit.close()
