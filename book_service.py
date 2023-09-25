# book_service.py

from pymongo import MongoClient
from config import MONGO_URI, DATABASE_NAME, COLLECTION_NAME, REQUIRED_FIELDS

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


def validate_book_data(book_data):
    """Validate the incoming book data."""
    if not isinstance(book_data, dict):
        raise ValueError("Invalid book data format.")

    missing_fields = [field for field in REQUIRED_FIELDS if field not in book_data]
    if missing_fields:
        raise ValueError(f"Missing required fields: {', '.join(missing_fields)}")

    # Add more validation if needed, like type checks or content checks


def update_book_by_isbn(isbn, updated_data):
    """Update a book in the collection based on its ISBN."""
    try:
        # Check for the number of books with the given ISBN
        count = collection.count_documents({"ean_isbn13": isbn})

        if count == 0:
            raise ValueError(f"No book found with ISBN {isbn}.")
        elif count > 1:
            raise ValueError(f"Multiple books found with ISBN {isbn}. Update aborted.")

        # Update the book data
        collection.update_one({"ean_isbn13": isbn}, {"$set": updated_data})

        return collection.find_one({"ean_isbn13": isbn})

    except Exception as e:
        raise DatabaseError(f"Error updating book with ISBN {isbn}: {str(e)}") from e

def delete_book_by_isbn(isbn):
    """Delete a book from the collection based on its ISBN."""
    try:
        result = collection.delete_one({"ean_isbn13": isbn})

        # The 'deleted_count' attribute indicates how many documents were deleted
        if result.deleted_count == 1:
            return True
        else:
            return False

    except Exception as e:
        raise DatabaseError(f"Error deleting book with ISBN {isbn}: {str(e)}") from e


def ensure_text_index():
    """Ensure the text index exists for searching."""
    collection.create_index([
        ("ean_isbn13", "text"),
        ("title", "text"),
        ("creators", "text"),
        ("firstName", "text"),
        ("lastName", "text"),
        ("description", "text"),
        ("publisher", "text")
    ])

def search_books(query):
    """Search for books based on a text query."""
    try:
        books_cursor = collection.find({
            "$text": {
                "$search": query
            }
        })
        books = list(books_cursor)

        # Convert ObjectId to string for serialization
        for book in books:
            book["_id"] = str(book["_id"])

            # Convert ean_isbn13 to integer, if it exists and is a float
            if "ean_isbn13" in book and isinstance(book["ean_isbn13"], float):
                book["ean_isbn13"] = int(book["ean_isbn13"])

        return books

    except Exception as e:
        raise DatabaseError(f"Error searching for books: {str(e)}") from e


def get_books_by_author(author_name):
    """Retrieve books from the collection written by a specific author."""
    try:
        # Splitting the author_name on spaces
        name_parts = author_name.split()

        # Creating regex search criteria for each part
        search_criteria = [{"creators": {"$regex": part, "$options": 'i'}} for part in name_parts]

        # Using the $and operator to ensure all parts are present
        books_cursor = collection.find({
            "$and": search_criteria
        })

        books = list(books_cursor)

        # Convert ObjectId to string for serialization
        for book in books:
            book["_id"] = str(book["_id"])

        return books

    except Exception as e:
        raise DatabaseError(f"Error fetching books by author {author_name}: {str(e)}") from e


def get_random_book():
    """Retrieve a random book from the collection."""
    try:
        books_cursor = collection.aggregate([
            {"$sample": {"size": 1}}
        ])
        book = next(books_cursor, None)

        if book:
            # Convert ObjectId to string for serialization
            book["_id"] = str(book["_id"])

        return book

    except Exception as e:
        raise DatabaseError(f"Error fetching a random book: {str(e)}") from e


def initialize_db():
    """Initialize the database with required indexes and other setup."""
    ensure_text_index()
    # Any other DB setup can go here
