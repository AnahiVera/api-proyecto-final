import cloudinary.uploader
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import User, Profile, Ranking, Application, rankingApplications, db
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
    avatarFile = None
    avatarResp = None

    resumeFile = None
    resumeResp = None



    id = get_jwt_identity()
    user = User.query.get(id)
    
    if 'avatar' in request.files:
        avatarFile = request.files['avatar']
        if user.profile.public_id:
            avatarResp = cloudinary.uploader.upload(avatarFile, public_id=user.profile.public_id)
        else:
            avatarResp = cloudinary.uploader.upload(avatarFile, folder="profiles_users")


    if 'resume' in request.files:
        resumeFile = request.files['resume']
        if user.profile.file_id:
            resumeResp = cloudinary.uploader.upload(resumeFile, public_id=user.profile.file_id)
        else:
            resumeResp = cloudinary.uploader.upload(resumeFile, folder="ResumeUser")
            


  
    user.profile.biography = request.form['biography'] if 'biography' in request.form else user.profile.biography
    user.profile.github = request.form['github'] if 'github' in request.form else user.profile.github
    user.profile.linkedin = request.form['linkedin'] if 'linkedin' in request.form else user.profile.linkedin
    user.profile.phone = request.form['phone'] if 'phone' in request.form else user.profile.phone
    user.profile.country = request.form['country'] if 'country' in request.form else user.profile.country


    user.profile.avatar = avatarResp['secure_url'] if avatarResp is not None else user.profile.avatar
    user.profile.public_id = avatarResp['public_id'] if avatarResp is not None else user.profile.public_id
    
    
    user.profile.resume = resumeResp['secure_url'] if resumeResp is not None else user.profile.resume
    user.profile.file_id = resumeResp['public_id'] if resumeResp is not None else user.profile.file_id

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


@bp_profile.route('/profile/rank_app', methods=['POST'])
@jwt_required()
def rank_application():
    
    data = request.get_json()

    print(data)

    user_id = data.get("user_id")
    ranking_id = data.get("ranking_id")
    application_id = data.get("application_id")

    application = Application.query.filter_by(id=application_id).first()

    if not user_id or not ranking_id or not application_id:
        return jsonify({"error": "Faltan campos requeridos"}), 400

    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "Usuario no encontrado"}), 404


    ranking = Ranking.query.get(ranking_id)
    if not ranking:
        return jsonify({"error": "Ranking no encontrado"}), 404
    
    insert_stmt = rankingApplications.insert().values(ranking_id=ranking_id, user_id=user_id, application_id=application_id)
    db.session.execute(insert_stmt)
    db.session.commit()

    application.rated=True
    application.update()

    return jsonify({'status':'success','title':'Applicant Rated',"message":"Ranking de Application created successfully"}), 201