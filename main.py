'''main.py'''

from flask import Flask, jsonify
from pymongo import MongoClient
from config import MONGO_URI, DATABASE_NAME, COLLECTION_NAME

from book_service import get_book_by_isbn #get_book_route(isbn):
from book_service import get_all_books, DatabaseError #get_books_route()

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





if __name__ == '__main__':
    app.run(debug=True)
