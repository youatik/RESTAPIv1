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


def add_book(book_data):
    """Insert a new book into the collection."""
    try:
        # Ensure the ean_isbn13 is of type int
        if "ean_isbn13" in book_data:
            book_data["ean_isbn13"] = int(book_data["ean_isbn13"])

        result = collection.insert_one(book_data)
        return str(result.inserted_id)
    except Exception as e:
        raise DatabaseError(f"Error adding new book: {str(e)}") from e

REQUIRED_FIELDS = [
    "ean_isbn13",
    "title",
    "creators",
    "firstName",
    "lastName",
    "description",
    "publisher",
    "publishDate",
    "price",
    "length"
]

def validate_book_data(book_data):
    """Validate the incoming book data."""
    if not isinstance(book_data, dict):
        raise ValueError("Invalid book data format.")

    missing_fields = [field for field in REQUIRED_FIELDS if field not in book_data]
    if missing_fields:
        raise ValueError(f"Missing required fields: {', '.join(missing_fields)}")

    # Add more validation if needed, like type checks or content checks
