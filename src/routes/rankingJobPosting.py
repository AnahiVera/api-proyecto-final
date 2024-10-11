""" from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import rankingJobPosting, User, JobPosting

bp_rankingJobPosting = Blueprint('bp_rankingJobPosting', __name__)


@bp_rankingJobPosting.route('/rankingJobPosting', methods=['GET'])
@jwt_required()
def get_ranking_job_postings():
    user_id = get_jwt_identity()  
    user = User.query.get(user_id)

    if not user:
        return jsonify({"status": "error", "message": "User not found"}), 404

    
    rankings = RankingJobPosting.query.filter_by(user_id=user_id).all()
    rankings_serialized = [ranking.serialize() for ranking in rankings]

    return jsonify({"status": "success", "rankings": rankings_serialized}), 200





@bp_rankingJobPosting.route('/rankingJobPosting', methods=['POST'])
@jwt_required()
def create_ranking_job_posting():
    user_id = get_jwt_identity()  

    user = User.query.get(user_id)
    if not user:
        return jsonify({"status": "error", "message": "User not found"}), 404

  
    ranking = request.json.get('ranking')
    job_posting_id = request.json.get('jobPosting_id')


    if not ranking:
        return jsonify({"status": "error", "message": "Missing required fields: ranking"}), 422
    
    
    if not job_posting_id:
        return jsonify({"status": "error", "message": "Missing required fields: jobPosting ID"}), 422

    
    job_posting = JobPosting.query.get(job_posting_id)
    if not job_posting:
        return jsonify({"status": "error", "message": "Job posting not found"}), 404


    new_ranking_job_posting = RankingJobPosting(
        user_id=user_id,
        ranking=ranking,
        jobPosting_id=job_posting_id
    )

    new_ranking_job_posting.save()

    return jsonify({
        "status": "success", "message": "Ranking for job posting created!", "ranking_job_posting": new_ranking_job_posting.serialize()}), 201
 """