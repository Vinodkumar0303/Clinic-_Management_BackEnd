from flask import Blueprint, Flask, request, jsonify
from pymongo import MongoClient
from werkzeug.security import check_password_hash
from flask_cors import CORS
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

login_bp = Blueprint('login', __name__)
CORS(login_bp)  # Enable CORS for this Blueprint

# Load MongoDB URI and secret key from environment variables
mongo_uri = os.getenv('MONGO_URI')
client = MongoClient(mongo_uri)
db = client.PersonalBudget
users = db.User  # Use the correct collection name

@login_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    # Find the user by email
    user = users.find_one({'email': email})
    if user and check_password_hash(user['password'], password):
        return jsonify({"message": "Login successful"}), 200
    else:
        return jsonify({"message": "Invalid email or password"}), 401

# Register the blueprint
app.register_blueprint(login_bp)

if __name__ == '__main__':
    app.run(debug=True)
