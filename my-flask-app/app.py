from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
import os
from pymongo import MongoClient

# Load environment variables from the .env file
load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable CORS for the whole app

# Load the SECRET_KEY from environment variables
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

# Load the MongoDB URI from environment variables
mongo_uri = os.getenv('MONGO_URI')
client = MongoClient(mongo_uri)

# Use the 'PersonalBudget' database
db = client.PersonalBudget

# Register blueprints for authentication
from auth.register import register_bp
from auth.login import login_bp

app.register_blueprint(register_bp, url_prefix='/api')
app.register_blueprint(login_bp, url_prefix='/api')

if __name__ == '__main__':
    app.run(debug=True)
