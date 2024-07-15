from flask import Flask, request, jsonify
import os
from connection import getDataFromDB
from flask_cors import CORS
from dotenv import load_dotenv # type: ignore
load_dotenv()

SECRET_API_KEY = os.getenv('SECRET_API_KEY')
APP_PORT = os.getenv('APP_PORT')
DEBUG = os.getenv('DEBUG')

app = Flask(__name__)    
CORS(app, 
     #origins=["http://example.com", "http://another.com"],
     methods=["HEAD", "POST", "OPTIONS"],
     allow_headers=["Content-Type", "X-Api-Key"],
     supports_credentials=False,
     max_age=3600)

def isValidHeaderApiKey(request):
    auth_header = request.headers.get('X-Api-Key')
    if auth_header != SECRET_API_KEY:
        return False
    return True


@app.route('/account', methods=["POST"])
def getNetworkByAccountID():
    isValidHeaderApiKey(request)
    if not isValidHeaderApiKey(request):
        return jsonify({"error": "Invalid Api Key"}), 400
    try:
        dataOnJSON = request.json
        accountId = dataOnJSON.get("accountId")
        if not accountId:
            return jsonify({"error": "Missing AccountId in request"}), 400
        network = getDataFromDB(accountId)
        print(network)
        return jsonify(network), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

if __name__ == '__main__':
    app.run(port=APP_PORT, debug=DEBUG)
