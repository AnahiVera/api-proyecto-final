from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import TechKnowledge, JobPosting, Rank, Technologies

bp_tech_knowledge = Blueprint('bp_tech_knowledge', __name__)


@bp_tech_knowledge.route('/tech_knowledges', methods=['GET'])
@jwt_required()
def get_all_tech_knowledges():
    tech_knowledges = TechKnowledge.query.all()
    serialized = [tech.serialize() for tech in tech_knowledges]
    return jsonify({"status": "success", "tech_knowledges": serialized}), 200




@bp_tech_knowledge.route('/tech_knowledges', methods=['POST'])
@jwt_required()
def create_tech_knowledge():
    user_id = get_jwt_identity()

    job_posting_id = request.json.get('job_posting_id')
    rank_id = request.json.get('rank_id')
    technologies_id = request.json.get('technologies_id')


    if not job_posting_id or not rank_id or not technologies_id:
        return jsonify({"status": "error", "message": "Missing required fields"}), 422


    job_posting = JobPosting.query.get(job_posting_id)
    if not job_posting:
        return jsonify({"status": "error", "message": "JobPosting not found"}), 404

    rank = Rank.query.get(rank_id)
    if not rank:
        return jsonify({"status": "error", "message": "Rank not found"}), 404

    technology = Technologies.query.get(technologies_id)
    if not technology:
        return jsonify({"status": "error", "message": "Technology not found"}), 404


    new_tech_knowledge = TechKnowledge(
        job_posting_id=job_posting_id,
        rank_id=rank_id,
        technologies_id=technologies_id
    )

    new_tech_knowledge.save()

    return jsonify({"status": "success", "message": "Tech knowledge created", "tech_knowledge": new_tech_knowledge.serialize()}), 201
