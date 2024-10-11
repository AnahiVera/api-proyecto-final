from flask import Blueprint, request, jsonify
from models import Rank, tech_knowledges, db
from flask_jwt_extended import jwt_required, get_jwt_identity

bp_ranks = Blueprint('bp_ranks', __name__)

@bp_ranks.route('/ranks', methods=['GET'])
@jwt_required()
def get_ranks():
    ranks = Rank.query.all()

    serialized_ranks = [rank.serialize()for rank in ranks]

    return jsonify({"status": "success", "ranks": serialized_ranks}), 200


@bp_ranks.route('/ranks', methods=['POST'])
@jwt_required()
def create_ranks():
    data = request.json
    rank_name = data.get('name')
    

    if not rank_name:
        return jsonify({"status": "error", "message": "El nombre del rank es requerido"}), 400

    existing_rank = Rank.query.filter_by(name=rank_name).first()
    if existing_rank:
        return jsonify({"status": "error", "message": "El rank ya existe"}), 400


    new_rank = Rank(name=rank_name)

    try:
        # Insertar en la base de datos
        db.session.add(new_rank)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"status": "error", "message": str(e)}), 500

    return jsonify({"status": "success", "rank": new_rank.serialize()}), 201