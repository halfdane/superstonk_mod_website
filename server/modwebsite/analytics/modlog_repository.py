from collections import namedtuple

from quart import current_app


MOD_ACTIVITIES = ['approvelink', 'approvecomment', 'removelink', 'removecomment', 'spamlink', 'spamcomment', 'banuser', 'addcontributor']


async def fetch_mods():
    async with current_app.sqlite_db.execute("select distinct mod from modlog") as cursor:
        return [row[0] async for row in cursor]


async def fetch_modlog_old():
    day = 60 * 60 * 24
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


async def fetch_modlog():
    day = 60 * 60 * 24
    week = day * 7

    term = week
    term_times = term * 1_000
    sql = f"""
            select (created_utc / {term}) * {term_times} as day, mod, action, count(*) as count from modlog
            where 
            action in ({", ".join(["'"+activity+"'" for activity in MOD_ACTIVITIES])})
            group by mod, action, day
            order by day, mod
        """
    async with current_app.sqlite_db.execute(sql) as cursor:
        return [row async for row in cursor]


async def store_modlog(log):
    data = (log.id, log.action, log.mod.name, log.details, log.target_body, log.target_title, log.target_permalink,
            log.target_author, log.created_utc, 0)
    await current_app.sqlite_db.execute('''
        INSERT INTO modlog(id, action, mod, details, target_body, target_title, target_permalink, target_author, created_utc, timestamp_db_updated) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?) 
        ON CONFLICT(id) DO NOTHING''', data)
    await current_app.sqlite_db.commit()
