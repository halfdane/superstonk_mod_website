from collections import namedtuple

from quart import current_app


async def fetch_mods():
    async with current_app.sqlite_db.execute("select distinct mod from modlog") as cursor:
        return [row[0] async for row in cursor]


async def fetch_modlog():
    day = 60*60*24
    week = day * 7

    term = week
    term_times = term * 1_000
    async with current_app.sqlite_db.execute(f"""
            select (created_utc / {term}) * {term_times} as day, mod, count(*) as total from modlog
            where 
            action in ('approvelink', 'approvecomment', 'removelink', 'removecomment', 'spamlink', 'spamcomment', 'banuser', 'addcontributor')
            group by mod, day
            order by day, mod
        """) as cursor:
        Log = namedtuple("Log", "interval mod total")
        return [Log(row[0], row[1], row[2]) async for row in cursor]
