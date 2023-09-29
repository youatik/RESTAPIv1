# config.py
PORT = 5001
PROXY_PORT = 5002   # new port for the proxy API
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
