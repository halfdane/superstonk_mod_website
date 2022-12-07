import json

from quart import Blueprint, current_app, websocket
from quart_discord import requires_authorization

mod_activity_bp = Blueprint('mod_activity', __name__)


@mod_activity_bp.websocket("/mod_activity")
@requires_authorization
async def random_endpoint() -> None:
    data_ = await fetch_data()
    await websocket.send(json.dumps(data_))


async def fetch_data():
    async with current_app.db.connection() as connection:
        db_rows = await connection.fetch_all("""
        select DATE_TRUNC('day', created_utc) as day, mod, count(*) as total from modlog
        where created_utc BETWEEN now() - INTERVAL '50 days' and now() 
        and action in ('approvelink', 'approvecomment', 'removelink', 'removecomment', 'spamlink', 'spamcomment', 'banuser', 'addcontributor')
        group by mod, day
        order by day, mod""")
        rows = [{'day': row.day.timestamp() * 1000, 'mod': row.mod, 'cnt': row.total} for row in db_rows]
        return rows

