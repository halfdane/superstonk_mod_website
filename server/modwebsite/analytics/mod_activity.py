import json

from quart import Blueprint, current_app, websocket
from quart_discord import requires_authorization

mod_activity_bp = Blueprint('mod_activity', __name__)

NON_TEAM = [
    'Anti-Evil Operations',
    'AssistantBOT1',
    'Automatic_Papaya',
    'AutoModerator',
    'Cardioclaw',
    'nakimushinakimushi',
    'reddit',
    'Reddit Legal',
    'Satori-Blue-Shell',
    'Satori-Knee-Arrow',
    'Superstonk-Flairy',
    'Superstonk_QV',
    'Superstonk__QV',
    'zwakenberg',
]

FORMER_MEMBERS = [
    'Bradduck_Flyntmoore',
    'ButtFarm69',
    'DisproportionateWill',
    'catto_del_fatto',
    'jsmar18',
    'sharkbaitlol'
]




@mod_activity_bp.websocket('/mod_activity')
@requires_authorization
async def random_endpoint() -> None:
    await websocket.send(json.dumps(await fetch_data()))


@mod_activity_bp.websocket("/mod_activity_egraph")
@requires_authorization
async def mod_activity_egraph() -> None:
    # qs = urlparse.parse_qs(websocket.query_string.decode())
    # if qs['admin'] == ['true']:
    #     print('is an admin request')

    await websocket.send(json.dumps(await fetch_egraph_data()))


async def fetch_data():
    mods, buckets = await mods_and_buckets_from_db()
    series = []
    for timestamp, day_bucket in buckets.items():
        day_series = [timestamp]
        day_series.extend([day_bucket[mod] for mod in mods])
        series.append(day_series)

    labels = ['date']
    labels.extend(mods)

    return {
        "series": series,
        "meta": {"labels": labels}
    }


async def fetch_egraph_data():
    mods, series = await mods_and_buckets_from_db()
    mod_buckets = {}
    for day, day_bucket in series.items():
        for mod, total in day_bucket.items():
            day_entry = mod_buckets.get(mod, [])
            day_entry.append([day, total])
            mod_buckets[mod] = day_entry

    # mod_buckets =
    # {
    #   mod1: [[day, total], [day, total], [day, total]]
    #   mod2: [[day, total], [day, total], [day, total]]
    # }


    # return [{
    #     name: 'mod name ',
    #     data: [[day, total], [day, total], [day, total]]
    # }];
    return [{'name': mod, 'data': mod_bucket} for mod, mod_bucket in mod_buckets.items()]


async def mods_and_buckets_from_db():
    async with current_app.db.connection() as connection:
        mod_rows = await connection.fetch_all("select distinct mod from modlog")
        mods = [row.mod for row in mod_rows if row.mod not in NON_TEAM and row.mod not in FORMER_MEMBERS]
        mods = sorted(mods, key=str.casefold)
        mods = ['FORMER-MODS'] + mods + ['NON-TEAM']

        db_rows = await connection.fetch_all("""
            select DATE_TRUNC('day', created_utc) as day, mod, count(*) as total from modlog
            where 
            action in ('approvelink', 'approvecomment', 'removelink', 'removecomment', 'spamlink', 'spamcomment', 'banuser', 'addcontributor')
            group by mod, day
            order by day, mod""")
        # {"day": 1666044000000.0, "mod": "AutoModerator", "cnt": 468},
        #       {
        #         series: [
        #                 [1,10,100],
        #                 [2,20,80],
        #                 [3,50,60],
        #                 [4,70,80]
        #               ],
        #         meta: { labels: [ "x", "A", "B" ] }
        #        }

        buckets = {}
        for row in db_rows:
            timestamp_ = row.day.timestamp() * 1000
            day_bucket = buckets.get(timestamp_, {mod: 0 for mod in mods})
            if row.mod in NON_TEAM:
                mod = 'NON-TEAM'
            elif row.mod in FORMER_MEMBERS:
                mod = 'FORMER-MODS'
            else:
                mod = row.mod
            day_bucket[mod] += row.total
            buckets[timestamp_] = day_bucket


        # buckets =
        # day: {
        #       'mod1': 0,
        #       'mod2': 21,
        #   }
        return mods, buckets
