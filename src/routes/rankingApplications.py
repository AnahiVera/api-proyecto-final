""" from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import rankingApplications, User, Application

bp_rankingApplications = Blueprint('bp_rankingApplications', __name__)


@bp_rankingApplications.route('/rankingApplications', methods=['GET'])
@jwt_required()
def get_ranking_applications():
    user_id = get_jwt_identity()  
    user = User.query.get(user_id)

    if not user:
        return jsonify({"status": "error", "message": "User not found"}), 404

   
    ranking_applications = rankingApplications.query.filter_by(user_id=user_id).all()
    ranking_applications_serialized = [ranking.serialize() for ranking in ranking_applications]

    return jsonify({"status": "success", "ranking_applications": ranking_applications_serialized}), 200





@bp_rankingApplications.route('/rankingApplications', methods=['POST'])
@jwt_required()
def create_ranking_application():
    user_id = get_jwt_identity() 

    user = User.query.get(user_id)
    if not user:
        return jsonify({"status": "error", "message": "User not found"}), 404

    ranking = request.json.get('ranking')
    application_id = request.json.get('application_id')
  
    if not ranking:
        return jsonify({"status": "error", "message": "Missing required fields: ranking"}), 422
    
    if not application_id:
        return jsonify({"status": "error", "message": "Missing required fields: application ID"}), 422
    
    application = Application.query.get(application_id)
    if not application:
        return jsonify({"status": "error", "message": "Application not found"}), 404


    new_ranking_application = rankingApplications(
        user_id=user_id,
        ranking=ranking,
        application_id=application_id
    )

    new_ranking_application.save()

    return jsonify({
        "status": "success", "message": "Ranking for application created!","ranking_application": new_ranking_application.serialize() }), 201
 """