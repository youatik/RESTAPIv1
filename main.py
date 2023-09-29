import connexion
from config import PORT
from book_service import initialize_db
from book_logic import (
    get_books_logic,
    get_book_logic,
    add_book_logic,
    update_book_logic,
    delete_book_logic,
    search_books_logic,
    get_books_by_author_logic,
    get_random_book_logic
)

initialize_db()
app = connexion.App(__name__)

@app.route('/books', methods=['GET'])
def get_books_route():
    return get_books_logic()

@app.route('/books/isbn/<int:isbn>', methods=['GET'])
def get_book_route(isbn):
    return get_book_logic(isbn)

@app.route('/books', methods=['POST'])
def add_book_route():
    return add_book_logic()

@app.route('/books/isbn/<int:isbn>', methods=['PUT', 'PATCH'])
def update_book_route(isbn):
    return update_book_logic(isbn)

@app.route('/books/isbn/<int:isbn>', methods=['DELETE'])
def delete_book_route(isbn):
    return delete_book_logic(isbn)

@app.route('/books/search', methods=['GET'])
def search_books_route():
    return search_books_logic()

@app.route('/books/author/<author_name>', methods=['GET'])
def get_books_by_author_route(author_name):
    return get_books_by_author_logic(author_name)

@app.route('/books/random', methods=['GET'])
def get_random_book_route():
    return get_random_book_logic()

app.add_api('books_api.yml')

if __name__ == '__main__':
    app.run(port=PORT, debug=True)
