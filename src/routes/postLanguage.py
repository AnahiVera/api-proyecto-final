from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import PostLanguage, JobPosting, Language, User

bp_post_language = Blueprint('bp_post_language', __name__)

@bp_post_language.route('/post_languages', methods=['GET'])
def get_all_post_languages():
    post_languages = PostLanguage.query.all()
    serialized = [pl.serialize() for pl in post_languages]
    return jsonify({"status": "success", "post_languages": serialized}), 200




@bp_post_language.route('/post_languages', methods=['POST'])
@jwt_required()
def create_post_language():
    user_id = get_jwt_identity()

    job_posting_id = request.json.get('job_posting_id')
    language_id = request.json.get('language_id')


    if not job_posting_id or not language_id:
        return jsonify({"status": "error", "message": "Missing required fields"}), 422

  
    job_posting = JobPosting.query.get(job_posting_id)
    if not job_posting:
        return jsonify({"status": "error", "message": "JobPosting not found"}), 404

    language = Language.query.get(language_id)
    if not language:
        return jsonify({"status": "error", "message": "Language not found"}), 404


    new_post_language = PostLanguage(
        job_posting_id=job_posting_id,
        language_id=language_id
    )

    new_post_language.save()

    return jsonify({"status": "success", "message": "Post language created", "post_language": new_post_language.serialize()}), 201
