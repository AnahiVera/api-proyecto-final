from flask import Blueprint, request, jsonify

bp_ranks = Blueprint('bp_ranks', __name__)

@bp_ranks.route('/ranks', methods=['GET'])
def get_ranks():
    ranks = Rank.query.all()
    return jsonify({"status": "success", "ranks": ranks.serialize()}), 200

