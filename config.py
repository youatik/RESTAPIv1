# config.py

# ports for the API and proxy API
PORT = 5001
PROXY_PORT = 5002

# jwt key and secret
JWT_SECRET_KEY = "some_secret_key_here"
SHARED_SECRET = "your_shared_secret_here"

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
