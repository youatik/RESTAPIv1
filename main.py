# main.py
from flask import Flask
from book_service import initialize_db
from book_routes import book_bp

app = Flask(__name__)
initialize_db()

# Register the Blueprint
app.register_blueprint(book_bp)

if __name__ == '__main__':
    app.run(debug=True)
