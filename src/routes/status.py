from flask import Blueprint, request, jsonify
from models import Status, db
from flask_jwt_extended import jwt_required, get_jwt_identity

bp_status = Blueprint('bp_status', __name__)

@bp_status.route('/status', methods=['GET'])
@jwt_required()
def get_status():
    status = Status.query.all()
    return jsonify({"status": "success", "status": status.serialize()}), 200


@bp_status.route('/status', methods=['POST']) #para manejar crear application necesito insertar un status
@jwt_required()
def create_status():
    data = request.json
    status_name = data.get('name')

    if not status_name:
        return jsonify({"status": "error", "message": "El nombre del estado es requerido"}), 400

    # Crear un nuevo objeto Status
    new_status = Status(name=status_name)
    
    try:
        # Insertar en la base de datos
        db.session.add(new_status)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"status": "error", "message": str(e)}), 500

    return jsonify({"status": "success", "status": new_status.serialize()}), 201