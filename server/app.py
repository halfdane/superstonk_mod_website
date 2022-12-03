import asyncio
import time
import uuid
import random

from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sock import Sock

app = Flask(__name__, static_folder='../client/dist')

sock = Sock(app)


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


@app.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify('pong!')


@sock.route('/echo')
def echo(ws):
    while True:
        data = ws.receive()
        ws.send(data)


@sock.route('/random')
def random_endpoint(ws):
    while True:
        time.sleep(1)
        randint = random.randint(0, 999)
        print(f"sending {randint}")
        ws.send(randint)


@app.route('/', defaults={'path': 'index.html'})
@app.route('/<path:path>')
def catch_all(path):
    print(f"checking path {path}")
    return app.send_static_file(path)
