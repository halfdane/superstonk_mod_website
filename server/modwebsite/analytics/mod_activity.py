from modwebsite.analytics.modlog_updater import ModlogUpdater
from quart import Blueprint, request, session, current_app
from quart_discord import requires_authorization

from modwebsite.analytics.modlog_repository import MOD_ACTIVITIES, fetch_modlog, fetch_modlog_old, fetch_mods

NON_TEAM = [
    'Anti-Evil Operations',
    'AssistantBOT1',
    'Automatic_Papaya',
    'AutoModerator',
    'Cardioclaw',
    'ModCodeofConduct',
    'nakimushinakimushi',
    'reddit',
    'Reddit Legal',
    'Satori-Blue-Shell',
    'Satori-Knee-Arrow',
    'tweet_widget',
    'Superstonk-Flairy',
    'Superstonk_QV',
    'Superstonk__QV',
    'zwakenberg',
]


mod_activity_bp = Blueprint('mod_activity', __name__)


@mod_activity_bp.before_app_serving
def register() -> None:
    ModlogUpdater(current_app.reddit, current_app.scheduler)


@mod_activity_bp.route('/mod_activity')
@requires_authorization
async def mod_activity_endpoint():
    mods, source = await mods_and_buckets_from_db()

    superstonk_subreddit = await current_app.reddit.subreddit('superstonk')
    superstonk_moderators = [m.name async for m in superstonk_subreddit.moderator]

    return {
        'dataset': {'source': source},
        'moderators': superstonk_moderators,
        'nonTeam': NON_TEAM 
        }


async def mods_and_buckets_from_db():
    mod_rows = await fetch_mods()

    mods = [mod for mod in mod_rows]
    mods = sorted(mods, key=str.casefold)

    print("fetching logs")
    db_rows = await fetch_modlog()
    # day, mod, action, count

    # fill missing values (probably mod wasn't active on a given day) with 0
    buckets = {}
    for row in db_rows:
        timestamp_ = row[0]
        mod_activity_on_day = {mod: {activity: 0 for activity in MOD_ACTIVITIES} for mod in mods}
        day_bucket = buckets.get(timestamp_, mod_activity_on_day)
        day_bucket[row[1]][row[2]] += row[3]
        buckets[timestamp_] = day_bucket

    result = []
    for day, mod_activity_on_day in buckets.items():
        for mod, act in mod_activity_on_day.items():
            for activity, count in act.items():
                result.append([day, mod, activity, count])

    print(result[:100])

    # source: [
    #     [1649894400000, 'AutoModerator', 'removecomment', 237],
    #     [1649894400000, 'AutoModerator', 'removelink', 45]
    # ]


    return mods, result



@mod_activity_bp.route('/mod_activity_old')
@requires_authorization
async def mod_activity_endpoint_old():
    combine_non_team = request.args.get("combineNonTeam") == "true"
    combine_former_team = request.args.get("combineFormerTeam") == "true"
    combine_current_team = request.args.get("combineCurrentTeam") == "true"

    user_accessible = combine_non_team and combine_former_team and combine_current_team

    user = session['user']
    if not user_accessible and not user['is_admin']:
        return "Only available for moderators", 403

    mods, series = await mods_and_buckets_from_db_old(combine_non_team, combine_former_team, combine_current_team)

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
    return mod_activity


async def mods_and_buckets_from_db_old(combine_non_team, combine_former_team, combine_current_team):
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

    db_rows = await fetch_modlog_old()

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



