import json

from quart import Blueprint, current_app, request, session, g
from quart_discord import requires_authorization

from aiocache import cached, Cache
from aiocache.serializers import PickleSerializer

from modwebsite.analytics.modlog_repository import fetch_modlog, fetch_mods

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

app = current_app
mod_activity_bp = Blueprint('mod_activity', __name__)

#
#
# @mod_activity_bp.websocket('/mod_activity')
# @requires_authorization
# async def mod_activity_endpoint():
#     qs = urllib.parse.parse_qs(websocket.query_string.decode())
#
#     combine_non_team = qs.get("combineNonTeam", "true") == "true"
#     combine_former_team = qs.get("combineFormerTeam", "true") == "true"
#     combine_current_team = qs.get("combineCurrentTeam", "true") == "true"


@mod_activity_bp.route('/mod_activity')
@requires_authorization
async def mod_activity_endpoint():
    combine_non_team = request.args.get("combineNonTeam") == "true"
    combine_former_team = request.args.get("combineFormerTeam") == "true"
    combine_current_team = request.args.get("combineCurrentTeam") == "true"

    user = session['user']
    if (combine_non_team or combine_former_team or combine_current_team) and not user['is_admin']:
        return "Only available for moderators", 403

    mods, series = await mods_and_buckets_from_db(combine_non_team, combine_former_team, combine_current_team)

    # {
    #   mod1: [[day, total], [day, total], [day, total]]
    #   mod2: [[day, total], [day, total], [day, total]]
    # }
    mod_buckets = {}
    for day, day_bucket in series.items():
        for mod, total in day_bucket.items():
            day_entry = mod_buckets.get(mod, [])
            day_entry.append([day, total])
            mod_buckets[mod] = day_entry

    # return [{
    #     name: 'mod name ',
    #     data: [[day, total], [day, total], [day, total]]
    # }];
    mod_activity = [{'name': mod, 'data': mod_bucket} for mod, mod_bucket in mod_buckets.items()]
    print("done")
    return mod_activity


async def mods_and_buckets_from_db(combine_non_team, combine_former_team, combine_current_team):
    mod_rows = await fetch_mods()

    def combine_mod(mod):
        return (combine_non_team and mod in NON_TEAM) or \
               (combine_former_team and mod in FORMER_MEMBERS) or \
               (combine_current_team and mod not in FORMER_MEMBERS and mod not in NON_TEAM)

    mods = [mod for mod in mod_rows if not combine_mod(mod)]
    mods = sorted(mods, key=str.casefold)
    if combine_current_team:
        mods = ['TEAM'] + mods
    if combine_non_team:
        mods = mods + ['NON-TEAM']
    if combine_former_team:
        mods = ['FORMER-MODS'] + mods

    db_rows = await fetch_modlog()

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
        timestamp_ = row.interval
        day_bucket = buckets.get(timestamp_, {mod: 0 for mod in mods})
        if combine_non_team and row.mod in NON_TEAM:
            mod = 'NON-TEAM'
        elif combine_former_team and row.mod in FORMER_MEMBERS:
            mod = 'FORMER-MODS'
        elif combine_current_team and row.mod not in NON_TEAM and row.mod not in FORMER_MEMBERS:
            mod = 'TEAM'
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
