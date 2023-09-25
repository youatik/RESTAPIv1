# main.py
from flask import Flask
from book_service import initialize_db

app = Flask(__name__)
initialize_db()

from flask import Blueprint, jsonify, request
from book_service import (
    get_book_by_isbn,
    validate_book_data,
    update_book_by_isbn,
    get_all_books,
    DatabaseError,
    add_book,
    delete_book_by_isbn,
    search_books,
    get_books_by_author,
    get_random_book
)



from flask import Flask, request, jsonify

from book_service import initialize_db

from flask import Flask, jsonify, request
from flasgger import Swagger
from book_service import initialize_db


from flask import Flask
from book_service import initialize_db
from flasgger import Swagger


app = Flask(__name__)
swagger = Swagger(app)  # Initialize Flasgger with your Flask app
initialize_db()
@app.route('/books', methods=['GET'])
def get_books_route():
    """
    Retrieve all books
    ---
    tags:
      - Books
    responses:
      200:
        description: List of all books
      400:
        description: Database error
    """
    try:
        books = get_all_books()
        return jsonify(books)
    except DatabaseError as de:
        return jsonify({"error": str(de)}), 400


@app.route('/books/isbn/<int:isbn>', methods=['GET'])
def get_book_route(isbn):
    """
        Retrieve a book by its ISBN number
        ---
        tags:
          - Books
        parameters:
          - name: isbn
            in: path
            type: integer
            required: true
            description: ISBN number of the book
        responses:
          200:
            description: Returns the book with the specified ISBN
          404:
            description: Book not found
          400:
            description: Invalid input or other errors
        """
    try:
        book = get_book_by_isbn(isbn)
        if not book:
            return jsonify({"error": "Book not found"}), 404
        return jsonify(book)
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400


@app.route('/books', methods=['POST'])
def add_book_route():
    try:
        book_data = request.json
        validate_book_data(book_data)  # Validate before saving
        new_book_id = add_book(book_data)
        return jsonify({"message": "Book added successfully", "_id": new_book_id}), 201

    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400

    except DatabaseError as de:
        return jsonify({"error": str(de)}), 400


@app.route('/books/isbn/<int:isbn>', methods=['PUT', 'PATCH'])
def update_book_route(isbn):
    try:
        updated_data = request.json
        updated_book = update_book_by_isbn(isbn, updated_data)

        # Convert ObjectId to string for serialization
        updated_book["_id"] = str(updated_book["_id"])
        return jsonify(updated_book)

    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400

    except DatabaseError as de:
        return jsonify({"error": str(de)}), 400

@app.route('/books/isbn/<int:isbn>', methods=['DELETE'])
def delete_book_route(isbn):
    try:
        result = delete_book_by_isbn(isbn)
        if result:
            return jsonify({"message": f"Book with ISBN {isbn} deleted successfully"}), 200
        else:
            return jsonify({"error": f"No book found with ISBN {isbn}"}), 404
    except DatabaseError as de:
        return jsonify({"error": str(de)}), 400

@app.route('/books/search', methods=['GET'])
def search_books_route():
    query = request.args.get('q', '')
    try:
        books = search_books(query)
        return jsonify(books)
    except DatabaseError as de:
        return jsonify({"error": str(de)}), 400

@app.route('/books/author/<author_name>', methods=['GET'])
def get_books_by_author_route(author_name):
    try:
        books = get_books_by_author(author_name)
        return jsonify(books)
    except DatabaseError as de:
        return jsonify({"error": str(de)}), 400

@app.route('/books/random', methods=['GET'])
def get_random_book_route():
    try:
        book = get_random_book()
        if not book:
            return jsonify({"error": "No books available"}), 404
        return jsonify(book)
    except DatabaseError as de:
        return jsonify({"error": str(de)}), 400





if __name__ == '__main__':
    app.run(debug=True)
