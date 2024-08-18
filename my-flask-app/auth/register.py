from flask import Blueprint, request, jsonify
from pymongo import MongoClient
from werkzeug.security import generate_password_hash
from dotenv import load_dotenv
import os

load_dotenv()

register_bp = Blueprint('register', __name__)

# Load MongoDB URI from environment variable
mongo_uri = os.getenv('MONGO_URI')
client = MongoClient(mongo_uri)
db = client.PersonalBudget
users = db.User   # Use the collection name 'User'

@register_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    print(f"Received data: {data}")  # Debug print
    email = data.get('email')
    password = data.get('password')
    phone = data.get('phone')
    name = data.get('name')

    if users.find_one({'email': email}):
        print("User already exists")  # Debug print
        return jsonify({"message": "User already exists"}), 400

    hashed_password = generate_password_hash(password)
    result = users.insert_one({
        'email': email,
        'password': hashed_password,
        'phone': phone,
        'name': name
    })

    print(f"Inserted ID: {result.inserted_id}")  # Debug print
    return jsonify({"message": "User registered successfully"}), 201
