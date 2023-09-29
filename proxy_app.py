from flask import Flask, request, Response
import requests
import config  # Import the config file

app = Flask(__name__)

BASE_URL = f"http://localhost:{config.PORT}"  # Reading the main API port from config

@app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
def proxy(path):
    # Get the original request data and headers
    headers = {key: value for (key, value) in request.headers}
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
