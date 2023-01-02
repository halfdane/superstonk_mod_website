import logging

from quart import Blueprint, redirect, url_for, current_app, session, request
from quart_discord import DiscordOAuth2Session, Unauthorized, requires_authorization


discord_bp = Blueprint('discord_blueprint', __name__, url_prefix="/session")
logger = logging.getLogger(__name__)


@discord_bp.before_app_serving
async def create_discord_oauth2_session():
    discord_config = current_app.modwebsite_config['discord']
    discord_bp.discord = DiscordOAuth2Session(
        current_app,
        client_id=discord_config['discord_client_id'],
        client_secret=discord_config['discord_client_secret'],
        redirect_uri=discord_config['discord_redirect_uri'],
        bot_token=discord_config['discord_bot_token']
    )


async def fetch_user_roles_from_api(guild_id):
    route = f"/users/@me/guilds/{guild_id}/member"
    payload = await discord_bp.discord.request(route)
    return [int(v) for v in payload.get("roles", [])]


async def fetch_guild_roles_from_api(guild_id):
    guild = await current_app.discord_client.fetch_guild(f"{guild_id}")
    return {role.id: role.name for role in guild.roles}


async def fetch_reddit_username():
    route = f"/users/@me/connections"
    payload = await discord_bp.discord.request(route)
    return [c['name'] for c in payload if c['type'] == 'reddit'][0]


async def welcome_user(user):
    dm_channel = await discord_bp.discord.bot_request("/users/@me/channels", "POST", json={"recipient_id": user.id})
    return await discord_bp.discord.bot_request(
        f"/channels/{dm_channel['id']}/messages", "POST",
        json={"content": "A new session just started. If you logged in, that's expected."}
    )


@discord_bp.get("/authentication_endpoint/")
async def authentication_endpoint():
    authentication_redirect = await discord_bp.discord.create_session(scope=["guilds", "identify", "connections"])
    return {'authentication_endpoint': authentication_redirect.location}


@discord_bp.get("/callback/")
async def callback():
    logger.info("Returning from discord: verifying the result")
    await discord_bp.discord.callback()
    logger.info("Logging in was successful. Checking the user")
    user = await discord_bp.discord.fetch_user()

    mod_guild = current_app.modwebsite_config['mod_guild']
    roles_with_access_allowed = [v for v in mod_guild["accessing_roles"].values()]

    logger.info("Fetching roles")
    user_roles = await fetch_user_roles_from_api(mod_guild['guild_id'])
    guild_roles = await fetch_guild_roles_from_api(mod_guild['guild_id'])
    accessing_guild_roles = {guild_roles[v]: v for k, v in mod_guild["accessing_roles"].items()}
    current_user_roles = [k for k, v in accessing_guild_roles.items() if v in user_roles]

    session['discord_roles'] = current_user_roles
    if len(current_user_roles) == 0:
        error = f"The user {user.name} has the roles {user_roles} " \
                f"in the guild {mod_guild['guild_id']} " \
                f"but needs one of these roles: {roles_with_access_allowed}!<br>" \
                f"<a href='/'>Try again!</a>"
        logger.error("Missing roles - revoking the discord session")
        discord_bp.discord.revoke()
        logger.error(error)
        return error
    logger.info(f"relevant roles: {current_user_roles}")

    reddit_username = await fetch_reddit_username()

    session['user'] = {
        'id': user.id,
        'name': user.name,
        'discriminator': user.discriminator,
        'avatar_url': user.avatar_url,
        'role': current_user_roles[0],
        'is_admin': 'admin' in current_user_roles,
        'is_dev': user.name == 'halfdane.eth',
        'reddit_username': reddit_username
    }
    logger.info(f"User was successfully logged in and stored in the session: {session['user']}")
    await welcome_user(user)
    return session['user']


@discord_bp.get("/")
@requires_authorization
async def current_session_information():
    return session['user']


@discord_bp.post("/")
@requires_authorization
async def adjust_current_session():
    data = await request.get_json()
    user = session['user']
    if user['is_dev']:
        user['is_admin'] = data['admin']
    session['user'] = user
    return user


@discord_bp.delete("/")
async def logout():
    if await discord_bp.discord.authorized:
        discord_bp.discord.revoke()
    session.clear()
    return {}


@discord_bp.app_errorhandler(Unauthorized)
async def redirect_unauthorized(e):
    return "Unauthorized", 403

