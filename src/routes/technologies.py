from flask import Blueprint, request, jsonify

bp_technologies = Blueprint('technologies', __name__)

@bp_technologies.route('/technologies', methods=['GET'])
def get_technologies():
    technologies = Technologies.query.all()
    return jsonify({"status": "success", "technologies": technologies.serialize()}), 200