import datetime
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from models import User, Profile
from werkzeug.security import generate_password_hash, check_password_hash

bp_auth = Blueprint("bp_auth", __name__)

@bp_auth.route('/login', methods=['POST'])
def login():
    email = request.json.get('email')
    password = request.json.get('password')

    if not email:
        return jsonify({"status": "error", "message": "Email is required"}), 422
    
    if not password:
        return jsonify({"status": "error", "message": "Password is required"}), 422

    found = User.query.filter_by(email=email).first()

    if not found:
        return jsonify({"status": "error", "message": "email/password are incorrects"}), 401
    
    if not check_password_hash(found.password, password):
        return jsonify({"status": "error", "message": "email/password are incorrects"}), 401

    if found:
        expire = datetime.timedelta(days=3)
        access_token = create_access_token(identity=found.id, expires_delta=expire)

        data = {
            "access_token": access_token,
            "user": found.serialize()
        }

        return jsonify({"status": "success", "message": "Login successfully", "data": data}), 200

    return jsonify({"status": "error", "message": "login fail, please contact with administrator"}), 400

@bp_auth.route('/register', methods=['POST'])
def register():

    email = request.json.get('email')
    password = request.json.get('password')

    if not email:
        return jsonify({"status": "error", "message": "Email is required"}), 422
    
    if not password:
        return jsonify({"status": "error", "message": "Password is required"}), 422

    found = User.query.filter_by(email=email).first()

    if found:
        return jsonify({"status": "error", "message": "Email is already in use!"}), 422
    
    profile = Profile()
    user = User()

    user.email = email
    user.password = generate_password_hash(password)
    user.profile = profile
    user.save()

    if user:
        expire = datetime.timedelta(days=3)
        access_token = create_access_token(identity=user.id, expires_delta=expire)

        data = {
            "access_token": access_token,
            "user": user.serialize()
        }

        return jsonify({"status": "success", "message": "Register successfully", "data": data}), 200

    return jsonify({"status": "error", "message": "register fail, please contact with administrator"}), 400