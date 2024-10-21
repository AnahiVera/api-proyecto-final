import cloudinary.uploader
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import User, Profile
from werkzeug.security import generate_password_hash, check_password_hash

bp_profile = Blueprint('bp_profile', __name__)


@bp_profile.route('/profile', methods=['GET'])
@jwt_required()
def profile():
    id = get_jwt_identity()
    user = User.query.get(id)
    return jsonify({"status": "success", "message": "Profile loaded",  "user": user.serialize()})


@bp_profile.route('/profile/<int:id>', methods=['GET'])
def profile_by_id(id):
    user = User.query.get(id)

    if not user:
        return jsonify({"status": "error", "message": "Post's user not found"}), 404

    return jsonify({"status": "success", "message": "Profile loaded",  "user": user.serialize()})



@bp_profile.route('/profile', methods=['PATCH'])
@jwt_required()
def update_profile():
    file = None
    resp = None

    id = get_jwt_identity()
    user = User.query.get(id)
    
    if 'avatar' in request.files:
        file = request.files['avatar']
        if user.profile.public_id:
            resp = cloudinary.uploader.upload(file, public_id=user.profile.public_id)
        else:
            resp = cloudinary.uploader.upload(file, folder="profiles_users")

    if 'resume' in request.files:
        file = request.files['resume']
        if user.profile.file_id:
            resp = cloudinary.uploader.upload(file, file_id=user.profile.file_id)
        else:
            resp = cloudinary.uploader.upload(file, folder="ResumeUser")

  
    user.profile.biography = request.form['biography'] if 'biography' in request.form else user.profile.biography
    user.profile.github = request.form['github'] if 'github' in request.form else user.profile.github
    user.profile.linkedin = request.form['linkedin'] if 'linkedin' in request.form else user.profile.linkedin
    user.profile.phone = request.form['phone'] if 'phone' in request.form else user.profile.phone
    user.profile.country = request.form['country'] if 'country' in request.form else user.profile.country

    user.profile.resume = resp['secure_url'] if resp is not None else user.profile.resume
    user.profile.avatar = resp['secure_url'] if resp is not None else user.profile.avatar
    user.profile.public_id = resp['public_id'] if resp is not None else user.profile.public_id
    user.profile.file_id = resp['file_id'] if resp is not None else user.profile.file_id

    password = request.form.get('password')
    if password:
        user.password = generate_password_hash(password)

    user.update()

    return jsonify({"status": "success", "message": "Profile updated!", "user": user.serialize() }), 200





@bp_profile.route('/profile', methods=['DELETE'])
@jwt_required()
def delete_profile():
    id = get_jwt_identity()  
    user = User.query.get(id)
    
    if not user or not user.profile:
        return jsonify({"status": "error", "message": "Profile not found"}), 404

    if user.profile.public_id:
        cloudinary.uploader.destroy(user.profile.public_id)

 
    user.profile.delete()

    return jsonify({"status": "success", "message": "Profile deleted!"}), 200
