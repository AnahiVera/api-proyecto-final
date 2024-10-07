import os
import cloudinary
from flask import Flask, request, jsonify
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from models import db
from dotenv import load_dotenv
from routes.auth import bp_auth
from routes.profile import bp_profile

load_dotenv()

cloudinary.config( 
  cloud_name = os.getenv('CLOUDINARY_CLOUD_NAME'), 
  api_key = os.getenv('CLOUDINARY_CLOUD_API_KEY'), 
  api_secret = os.getenv('CLOUDINARY_CLOUD_API_SECRET'),
  secure = True
)

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_TRACKS_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')

db.init_app(app)
Migrate(app, db)
jwt = JWTManager(app)
CORS(app)

app.register_blueprint(bp_auth, url_prefix="/api")
app.register_blueprint(bp_profile, url_prefix="/api")

@app.route('/')
def main():
    return jsonify({"message": "Server running successfully!"}), 200

if __name__ == '__main__':
    app.run()
