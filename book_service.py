'''book_service.py'''
from pymongo import MongoClient
from bson.objectid import ObjectId
from config import MONGO_URI, DATABASE_NAME, COLLECTION_NAME

client = MongoClient(MONGO_URI)
db = client[DATABASE_NAME]
collection = db[COLLECTION_NAME]

class DatabaseError(Exception):
    """Raised for generic database errors."""
    pass
# ... Other imports and setup ...

def get_all_books():
    """Retrieve all books from the collection."""
    try:
        books_cursor = collection.find({})
        books = list(books_cursor)

        # Convert ObjectId to string for serialization
        for book in books:
            book["_id"] = str(book["_id"])

            # Convert ean_isbn13 to integer, if it exists and is a float
            if "ean_isbn13" in book and isinstance(book["ean_isbn13"], float):
                book["ean_isbn13"] = int(book["ean_isbn13"])

        return books

    except Exception as e:
        raise DatabaseError(f"Error fetching all books: {str(e)}") from e


def get_book_by_isbn(isbn):
    """Retrieve a book from the collection based on its ISBN."""
    try:
        book = collection.find_one({"ean_isbn13": isbn})
        if book:
            book["_id"] = str(book["_id"])
            # Convert ean_isbn13 to integer
            book["ean_isbn13"] = int(book["ean_isbn13"])
        return book

    except Exception as e:
        raise ValueError(f"Error fetching book: {str(e)}") from e
