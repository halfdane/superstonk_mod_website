from flask import Blueprint, redirect, url_for
from flask_discord import DiscordOAuth2Session, Unauthorized


class DiscordBlueprint(Blueprint):
    discord = None

    def register(self, app: "Flask", options: dict) -> None:
        super().register(app, options)
        self.discord = DiscordOAuth2Session(
            app,
            client_id=app.modwebsite_config['discord']['discord_client_id'],
            client_secret=app.modwebsite_config['discord']['discord_client_secret'],
            redirect_uri=app.modwebsite_config['discord']['discord_redirect_uri'],
            bot_token=app.modwebsite_config['discord']['discord_bot_token']
        )


discord_auth_blueprint = DiscordBlueprint('discord_blueprint', __name__)


def welcome_user(user):
    dm_channel = discord_auth_blueprint.discord.bot_request("/users/@me/channels", "POST", json={"recipient_id": user.id})
    return discord_auth_blueprint.discord.bot_request(
        f"/channels/{dm_channel['id']}/messages", "POST", json={"content": "Thanks for authorizing the app!"}
    )


@discord_auth_blueprint.route("/login/")
def login():
    return discord_auth_blueprint.discord.create_session()


@discord_auth_blueprint.route("/callback/")
def callback():
    discord_auth_blueprint.discord.callback()
    user = discord_auth_blueprint.discord.fetch_user()
    welcome_user(user)
    return redirect(url_for("catch_all"))


@discord_auth_blueprint.app_errorhandler(Unauthorized)
def redirect_unauthorized(e):
    return redirect(url_for("discord_blueprint.login"))
