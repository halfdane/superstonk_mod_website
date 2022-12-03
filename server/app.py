import asyncio
import os
import time
import uuid
import random

from flask import Flask, jsonify, request, redirect, url_for, current_app
from flask_cors import CORS
from flask_sock import Sock
from flask_discord import DiscordOAuth2Session, requires_authorization, Unauthorized

from config import read_config


app = Flask(__name__, static_folder='../client/dist')
sock = Sock(app)


config = read_config()
app.secret_key = config['discord']['discord_client_id'].encode()

# OAuth2 must make use of HTTPS in production environment.
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "true"      # !! Only in development environment.

app.config["DISCORD_CLIENT_ID"] = config['discord']['discord_client_id']          # Discord client ID.
app.config["DISCORD_CLIENT_SECRET"] = config['discord']['discord_client_secret']  # Discord client secret.
app.config["DISCORD_REDIRECT_URI"] = config['discord']['discord_redirect_uri']    # URL to your callback endpoint.
app.config["DISCORD_BOT_TOKEN"] = config['discord']['discord_bot_token']          # Required to access BOT resources.
discord = DiscordOAuth2Session(app)

CORS(app, resources={r'/*': {'origins': '*'}})

BOOKS = [
    {
        'id': uuid.uuid4().hex,
        'title': 'On the Road',
        'author': 'Jack Kerouac',
        'read': True
    },
    {
        'id': uuid.uuid4().hex,
        'title': 'Harry Potter and the Philosopher\'s Stone',
        'author': 'J. K. Rowling',
        'read': False
    },
    {
        'id': uuid.uuid4().hex,
        'title': 'Green Eggs and Ham',
        'author': 'Dr. Seuss',
        'read': True
    }
]


def remove_book(book_id):
    for book in BOOKS:
        if book['id'] == book_id:
            BOOKS.remove(book)
            return True
    return False


def welcome_user(user):
    dm_channel = discord.bot_request("/users/@me/channels", "POST", json={"recipient_id": user.id})
    return discord.bot_request(
        f"/channels/{dm_channel['id']}/messages", "POST", json={"content": "Thanks for authorizing the app!"}
    )

@app.route("/login/")
def login():
    return discord.create_session()


@app.route("/callback/")
def callback():
    discord.callback()
    user = discord.fetch_user()
    welcome_user(user)
    return redirect(url_for(".catch_all"))


@app.errorhandler(Unauthorized)
def redirect_unauthorized(e):
    return redirect(url_for("login"))


@app.route("/heartbeat")
def heartbeat():
    return jsonify({"status": "healthy"})


@app.route('/books', methods=['GET', 'POST'])
def all_books():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        post_data = request.get_json()
        BOOKS.append({
            'id': uuid.uuid4().hex,
            'title': post_data.get('title'),
            'author': post_data.get('author'),
            'read': post_data.get('read')
        })
        response_object['message'] = 'Book added!'
    else:
        response_object['books'] = BOOKS
    return jsonify(response_object)


@app.route('/books/<book_id>', methods=['PUT', 'DELETE'])
def single_book(book_id):
    response_object = {'status': 'success'}
    if request.method == 'PUT':
        post_data = request.get_json()
        remove_book(book_id)
        BOOKS.append({
            'id': uuid.uuid4().hex,
            'title': post_data.get('title'),
            'author': post_data.get('author'),
            'read': post_data.get('read')
        })
        response_object['message'] = 'Book updated!'
    if request.method == 'DELETE':
        remove_book(book_id)
        response_object['message'] = 'Book removed!'
    return jsonify(response_object)


@sock.route('/random')
def random_endpoint(ws):
    if not discord.authorized:
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
