from flask import Blueprint, request, jsonify

bp_status = Blueprint('bp_status', __name__)

@bp_status.route('/status', methods=['GET'])
def get_status():
    status = Status.query.all()
    return jsonify({"status": "success", "status": status.serialize()}), 200