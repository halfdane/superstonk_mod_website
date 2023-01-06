import logging
from datetime import datetime, timedelta

from asyncpraw import Reddit
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from modwebsite.analytics.modlog_repository import store_modlog


class ModlogUpdater:
    def __init__(self, reddit: Reddit, scheduler: AsyncIOScheduler) -> None:
        self.subreddit = None
        self.logger = logging.getLogger(__name__)
        self.reddit = reddit
        scheduler.add_job(self.setup)
        # scheduler.add_job(self.fetch_all, next_run_time=datetime.now() + timedelta(seconds=5))
        scheduler.add_job(self.fetch_modlog_data, 'interval', seconds=10)

    async def setup(self):
        self.subreddit = await self.reddit.subreddit("Superstonk")

    async def fetch_all(self):
        self.logger.info("Fetching ALL modlog entries")
        async for log in self.subreddit.mod.log(limit=None):
            self.logger.info(f"log from {datetime.fromtimestamp(log.created_utc)}: {log.mod} {log.action}")
            await store_modlog(log)

    async def fetch_modlog_data(self):
        self.logger.info("Fetching new modlog entries")
        async for log in self.subreddit.mod.log(limit=100):
            await store_modlog(log)

