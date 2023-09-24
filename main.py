'''main.py'''

from flask import Flask, jsonify
from pymongo import MongoClient
from config import MONGO_URI, DATABASE_NAME, COLLECTION_NAME

from book_service import get_book_by_isbn, validate_book_data  # get_book_route(isbn): # add_book_route():
from book_service import get_all_books, DatabaseError #get_books_route()

from flask import request #add_book
from book_service import add_book #add_book


app = Flask(__name__)


@app.route('/books', methods=['GET'])
def get_books_route():
    try:
        books = get_all_books()
        return jsonify(books)

    except DatabaseError as de:
        return jsonify({"error": str(de)}), 400


@app.route('/books/isbn/<int:isbn>', methods=['GET'])
def get_book_route(isbn):
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






if __name__ == '__main__':
    app.run(debug=True)
