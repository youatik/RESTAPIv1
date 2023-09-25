# main.py
from flask import Flask
from book_service import initialize_db
from book_routes import book_bp
from flasgger import Swagger

app = Flask(__name__)

# Swagger configuration moved to main.py
swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": 'apispec_1',
            "route": '/apispec_1.json',
            "rule_filter": lambda rule: True,  # all in
            "model_filter": lambda tag: True,  # all in
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/swagger/",
}
Swagger(app, config=swagger_config)

app.register_blueprint(book_bp)

initialize_db()

if __name__ == '__main__':
    app.run(debug=True)
