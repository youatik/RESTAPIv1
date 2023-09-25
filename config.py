# config.py
# MongoDB configuration
MONGO_URI = "mongodb://localhost:27017/"
DATABASE_NAME = "A17"
COLLECTION_NAME = "Books"
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
