import uuid

from quart import Blueprint, request, jsonify

from modwebsite.books import services

books_blueprint = Blueprint('books', __name__)


@books_blueprint.route('/books', methods=['GET', 'POST'])
async def all_books():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        post_data = await request.get_json()
        services.BOOKS.append({
            'id': uuid.uuid4().hex,
            'title': post_data.get('title'),
            'author': post_data.get('author'),
            'read': post_data.get('read')
        })
        response_object['message'] = 'Book added!'
    else:
        response_object['books'] = services.BOOKS
    return jsonify(response_object)


@books_blueprint.route('/books/<book_id>', methods=['PUT', 'DELETE'])
async def single_book(book_id):
    response_object = {'status': 'success'}
    if request.method == 'PUT':
        post_data = await request.get_json()
        services.remove_book(book_id)
        services.BOOKS.append({
            'id': uuid.uuid4().hex,
            'title': post_data.get('title'),
            'author': post_data.get('author'),
            'read': post_data.get('read')
        })
        response_object['message'] = 'Book updated!'
    if request.method == 'DELETE':
        services.remove_book(book_id)
        response_object['message'] = 'Book removed!'
    return jsonify(response_object)
