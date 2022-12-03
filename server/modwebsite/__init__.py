import os
import random
import time

from flask import Flask, jsonify, current_app
from flask_cors import CORS
from flask_discord import requires_authorization
from flask_sock import Sock

from config import read_config
from modwebsite.auth import discord_auth_blueprint
from modwebsite.books import books_blueprint

app = Flask(__name__, static_folder='../../client/dist')
sock = Sock(app)

config = read_config()
app.modwebsite_config = config
app.secret_key = config['server']['flask_secret_key'].encode()

# OAuth2 must make use of HTTPS in production environment.
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "true"  # !! Only in development environment.

CORS(app, resources={r'/*': {'origins': '*'}})

app.register_blueprint(discord_auth_blueprint)
app.register_blueprint(books_blueprint)


@app.route("/heartbeat")
def heartbeat():
    return jsonify({"status": "healthy"})


@sock.route('/random')
def random_endpoint(ws):
    if not current_app.discord.authorized:
        ws.send("HTTP Authentication failed; remove your cookies and try to log in")
    else:
        while True:
            time.sleep(1)
            randint = random.randint(0, 999)
            print(f"sending {randint}")
            ws.send(randint)


@app.route('/', defaults={'path': 'index.html'})
@app.route('/<path:path>')
@requires_authorization
def catch_all(path):
    print(f"checking path {path}")
    return app.send_static_file(path)
