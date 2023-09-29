import connexion
from config import PORT, JWT_SECRET_KEY, SHARED_SECRET
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
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
from flask import jsonify, request

# Initialize database
initialize_db()

# Create a Connexion application instance
connexion_app = connexion.App(__name__)

# Get the underlying Flask app instance from Connexion app
app = connexion_app.app

# Configure JWT
app.config["JWT_SECRET_KEY"] = JWT_SECRET_KEY
jwt = JWTManager(app)

@app.route('/token', methods=['POST'])
def issue_token():
    secret = request.json.get('secret')
    if secret == SHARED_SECRET:
        access_token = create_access_token(identity="proxy_api")
        print("Generated Token:", access_token)
        return jsonify(access_token=access_token), 200
    else:
        return jsonify({"error": "Unauthorized"}), 401

@app.route('/books', methods=['GET'])
@jwt_required()
def get_books_route():
    return get_books_logic()

@app.route('/books/isbn/<int:isbn>', methods=['GET'])
@jwt_required()
def get_book_route(isbn):
    return get_book_logic(isbn)

@app.route('/books', methods=['POST'])
@jwt_required()
def add_book_route():
    return add_book_logic()

@app.route('/books/isbn/<int:isbn>', methods=['PUT', 'PATCH'])
@jwt_required()
def update_book_route(isbn):
    return update_book_logic(isbn)

@app.route('/books/isbn/<int:isbn>', methods=['DELETE'])
@jwt_required()
def delete_book_route(isbn):
    return delete_book_logic(isbn)

@app.route('/books/search', methods=['GET'])
@jwt_required()
def search_books_route():
    return search_books_logic()

@app.route('/books/author/<author_name>', methods=['GET'])
@jwt_required()
def get_books_by_author_route(author_name):
    return get_books_by_author_logic(author_name)

@app.route('/books/random', methods=['GET'])
@jwt_required()
def get_random_book_route():
    return get_random_book_logic()

# Connect the Swagger YAML file
connexion_app.add_api('books_api.yml')

if __name__ == '__main__':
    connexion_app.run(port=PORT, debug=True)
