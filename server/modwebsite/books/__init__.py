import uuid

from quart import Blueprint, request, jsonify

import modwebsite.books.book_service

books_blueprint = Blueprint('books', __name__)


@books_blueprint.route('/books', methods=['GET', 'POST'])
async def all_books():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        post_data = await request.get_json()
        book_service.BOOKS.append({
            'id': uuid.uuid4().hex,
            'title': post_data.get('title'),
            'author': post_data.get('author'),
            'read': post_data.get('read')
        })
        response_object['message'] = 'Book added!'
    else:
        response_object['books'] = book_service.BOOKS
    return jsonify(response_object)


@books_blueprint.route('/books/<book_id>', methods=['PUT', 'DELETE'])
async def single_book(book_id):
    response_object = {'status': 'success'}
    if request.method == 'PUT':
        post_data = await request.get_json()
        book_service.remove_book(book_id)
        book_service.BOOKS.append({
            'id': uuid.uuid4().hex,
            'title': post_data.get('title'),
            'author': post_data.get('author'),
            'read': post_data.get('read')
        })
        response_object['message'] = 'Book updated!'
    if request.method == 'DELETE':
        book_service.remove_book(book_id)
        response_object['message'] = 'Book removed!'
    return jsonify(response_object)
