import os
import random

from quart import Quart, websocket
from quart_cors import cors
from quart_discord import requires_authorization

from modwebsite import auth, analytics
from modwebsite.config.QuartDatabases import QuartDatabases
from modwebsite.books import books_blueprint
from modwebsite.config.configuration_reader import config


def create(test_config=None):
    app = Quart(__name__, static_folder='../../client/dist')
    app.modwebsite_config = config(app.env)

    app = cors(app,
               allow_origin=app.modwebsite_config['server']['allow_origin'],
               allow_credentials=app.modwebsite_config['server']['allow_credentials'])

    app.secret_key = app.modwebsite_config['server']['flask_secret_key'].encode()
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = app.modwebsite_config['server']['allow_insecure_transport_for_oauth']

    app.register_blueprint(auth.discord_bp)
    app.register_blueprint(books_blueprint)
    app.register_blueprint(analytics.mod_activity_bp)

    QuartDatabases(app)

    @app.route('/', defaults={'path': 'index.html'})
    @app.route('/<path:path>')
    @requires_authorization
    async def catch_all(path):
        return await app.send_static_file(path)

    return app

