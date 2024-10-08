from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import Application


bp_application = Blueprint('bp_application', __name__)

@bp_application.route('/applications', methods=['GET'])
@jwt_required()
def get_applications():
    user_id = get_jwt_identity()
    applications= Application.query.filter_by(user_id=user_id).all()

    if not applications:
        return jsonify({"status": "success", "message": "No applications found.", "applications": [] }), 200

    return jsonify({"status": "success", "message": "All applications found",  "applications": applications.serialize()}), 200

@bp_application.route('/applications', methods=['POST']) #aplicar a publicacion de trabajo
@jwt_required()
def apply_job()
    user_id = get_jwt_identity()
    data = request.json
    job_id = data.get('job_posting_id')
    job = JobPosting.query.get_or_404(job_id)

    already_applied= Application.query.filter_by(user_id=user_id, job_posting_id= job_id).first()
    if already_applied:
        return jsonify({"status": "error", "message": "You have already applied to this offer"}), 400
    
    new_application = Application (
        user_id=user_id,
        job_posting_id=job_id,
        status_id = 1
    )
    application.save()
    return jsonify({"status": "success", "You have applied": application.serialize()}), 201


@bp_application.route('/applications/<int:application_id>', methods=['GET']) # obtener applicacion en espeficifo get (id)
@jwt_required()
def get_application(application_id)
    user_id = get_jwt_identity()
    application = Application.query.get_or_404(application_id)


# el empleador debe poder actualizar el status (aceptar o rechazar, pendiente?) Patch (id) 
#el aplicante puede eliminar su aplicacion  delete