from flask import Flask, Response, jsonify
import requests
import config  # Import the config file
from flask_jwt_extended import JWTManager, create_access_token
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
from flask_jwt_extended import JWTManager
from flask import request




app = Flask(__name__)

BASE_URL = f"http://localhost:{config.PORT}"  # Reading the main API port from config
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

@app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
def proxy(path):
    access_token = get_token()
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    # Get the original request data and headers
    original_headers = {key: value for (key, value) in request.headers}
    headers.update(original_headers)
    data = request.data

    # Forward the request to the main API
    response = requests.request(
        method=request.method,
        url=f"{BASE_URL}/{path}",
        headers=headers,
        data=data
    )

    # Return the response from the main API
    return Response(response.content, response.status_code, response.headers.items())

if __name__ == '__main__':
    app.run(port=config.PROXY_PORT, debug=True)  # Reading the proxy API port from config
