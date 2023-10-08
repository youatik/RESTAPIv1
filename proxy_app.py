from flask import Flask, Response, jsonify
import requests
import config  # Import le fichier config
from flask_jwt_extended import JWTManager
from flask import request


app = Flask(__name__)

BASE_URL = f"http://localhost:{config.PORT}"
app.config["JWT_SECRET_KEY"] = config.JWT_SECRET_KEY
jwt = JWTManager(app)

token = None

def get_token():
    global token
    if not token:
        response = requests.post(
            f"{BASE_URL}/token",
            json={"secret": config.SHARED_SECRET}
        )
        data = response.json()
        token = data.get('access_token')
    return token

# Obtenir un token automatiquement en debut de session

get_token()

@app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
def proxy(path):
    access_token = get_token()
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    # Obtenir le request data et les headers
    original_headers = {key: value for (key, value) in request.headers}

    # Donner au JWT token la precedence
    original_headers["Authorization"] = f"Bearer {access_token}"
    headers = original_headers

    # Capturer le body et le content de l'incoming request
    data = request.data

    # Forwarder la request au base API
    response = requests.request(
        method=request.method,
        url=f"{BASE_URL}/{path}",
        headers=headers,
        data=data
    )

    # Retourner la response du base API
    return Response(response.content, response.status_code, response.headers.items())


if __name__ == '__main__':
    app.run(port=config.PROXY_PORT, debug=True)  # PORT proxy API du config
