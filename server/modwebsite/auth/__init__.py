from quart import Blueprint, redirect, url_for, current_app
from quart_discord import DiscordOAuth2Session, Unauthorized, requires_authorization


class DiscordBlueprint(Blueprint):
    discord = None

    def register(self, app: "Flask", options: dict) -> None:
        super().register(app, options)
        discord_config = app.modwebsite_config['discord']
        self.discord = DiscordOAuth2Session(
            app,
            client_id=discord_config['discord_client_id'],
            client_secret=discord_config['discord_client_secret'],
            redirect_uri=discord_config['discord_redirect_uri'],
            bot_token=discord_config['discord_bot_token']
        )


discord_bp = DiscordBlueprint('discord_blueprint', __name__)


async def fetch_roles_from_api(guild_id):
    route = f"/users/@me/guilds/{guild_id}/member"
    payload = await discord_bp.discord.request(route)
    return [int(v) for v in payload.get("roles", [])]


async def welcome_user(user):
    dm_channel = await discord_bp.discord.bot_request("/users/@me/channels", "POST", json={"recipient_id": user.id})
    return await discord_bp.discord.bot_request(
        f"/channels/{dm_channel['id']}/messages", "POST", json={"content": "Thanks for authorizing the app!"}
    )


@discord_bp.route("/login/")
async def login():
    return await discord_bp.discord.create_session(scope=["guilds.members.read"])


@discord_bp.route("/callback/")
async def callback():
    await discord_bp.discord.callback()
    user = await discord_bp.discord.fetch_user()

    mod_guild = current_app.modwebsite_config['mod_guild']
    roles_with_access_allowed = [v for v in mod_guild["accessing_roles"].values()]
    roles_current_user_has = await fetch_roles_from_api(mod_guild['guild_id'])

    roles_with_access_allowed_that_current_user_has = \
        [value for value in roles_with_access_allowed if value in roles_current_user_has]

    if len(roles_with_access_allowed_that_current_user_has) == 0:
        error = f"The user {user.name} has the roles {roles_current_user_has} " \
                f"in the guild {mod_guild['guild_id']} " \
                f"but needs one of these roles: {roles_with_access_allowed}!<br>" \
                f"<a href='/'>Try again!</a>"
        discord_bp.discord.revoke()
        return error

    await welcome_user(user)
    return redirect(url_for("catch_all"))


@discord_bp.route("/session/")
@requires_authorization
async def session():
    user = await discord_bp.discord.fetch_user()
    return {
        'name': user.name,
        'avatar_url': user.avatar_url
    }

@discord_bp.route("/session/", methods=['DELETE'])
async def logout():
    if await discord_bp.discord.authorized:
        discord_bp.discord.revoke()
    return redirect(url_for("catch_all"))


@discord_bp.app_errorhandler(Unauthorized)
async def redirect_unauthorized(e):
    return redirect(url_for("discord_blueprint.login"))
