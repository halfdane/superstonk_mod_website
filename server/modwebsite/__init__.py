import json
import os
import random

from quart import Quart, jsonify, websocket
from quart_cors import cors
from quart_discord import requires_authorization

from modwebsite import auth
from modwebsite.books import books_blueprint
from modwebsite.config import config


def create_app(test_config=None):
    app = Quart(__name__, static_folder='../../client/dist')
    app.modwebsite_config = config(app.env)

    app = cors(app,
               allow_origin=app.modwebsite_config['server']['allow_origin'],
               allow_credentials=app.modwebsite_config['server']['allow_credentials'])

    app.secret_key = app.modwebsite_config['server']['flask_secret_key'].encode()
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = app.modwebsite_config['server']['allow_insecure_transport_for_oauth']

    app.register_blueprint(auth.discord_bp)
    app.register_blueprint(books_blueprint)

    @app.websocket("/random")
    @requires_authorization
    async def random_endpoint() -> None:
        for i in range(5):
            randint = random.randint(0, 999)
            print(f"Sending random number {i}/{100}: {randint}")
            await websocket.send(f"{randint}")

    @app.route('/', defaults={'path': 'index.html'})
    @app.route('/<path:path>')
    @requires_authorization
    async def catch_all(path):
        return await app.send_static_file(path)

    return app
