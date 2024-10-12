from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import Application, JobPosting, Status


bp_application = Blueprint('bp_application', __name__)

@bp_application.route('/applications', methods=['GET'])
@jwt_required()
def get_applications():
    user_id = get_jwt_identity()
    applications = Application.query.filter_by(user_id=user_id).all()

    if not applications:
        return jsonify({"status": "success", "message": "No applications found.", "applications": []}), 200

    serialized_applications = [application.serialize() for application in applications]

    return jsonify({"status": "success", "message": "All applications found", "applications": serialized_applications}), 200

@bp_application.route('/applications', methods=['POST']) #aplicar a publicacion de trabajo
@jwt_required()
def apply_job():
    user_id = get_jwt_identity()
    data = request.json
    job_id = data.get('job_posting_id')
    job = JobPosting.query.get_or_404(job_id)

    if job.user_id == user_id:
        return jsonify({"status": "error", "message": "You cannot apply to your own job posting"}), 400

    already_applied= Application.query.filter_by(user_id=user_id, job_posting_id= job_id).first()
    if already_applied:
        return jsonify({"status": "error", "message": "You have already applied to this offer"}), 400
    
    application  = Application (
        user_id=user_id,
        job_posting_id=job_id,
        status_id = 1
        
    )
    application.save()
    return jsonify({"status": "success", "You have applied": application.serialize()}), 201


@bp_application.route('/applications/<int:application_id>', methods=['GET']) # obtener applicacion en espeficifo get (id)
@jwt_required()
def get_application(application_id):
    user_id = get_jwt_identity()
    application = Application.query.get_or_404(application_id)

    if application.user_id != user_id and application.job_posting.user_id != user_id:
        return jsonify({"status": "error", "message": "Not authorized"}), 403
    
    return jsonify({"status": "success", "application": application.serialize()}), 200


@bp_application.route('/applications/<int:application_id>', methods=['PATCH']) #el empleador debe poder actualizar el status (aceptar o rechazar, pendiente?) Patch (id) 
@jwt_required()
def update_application(application_id):

    user_id = get_jwt_identity()
    application = Application.query.get_or_404(application_id)
    
    # Solo el empleador de la publicación puede actualizar el estado
    if application.job_posting.user_id != user_id:
        return jsonify({"status": "error", "message": "Not authorized"}), 403
    
    data = request.json
    if 'status_id' in data:
        application.status_id = data['status_id']
    
    application.update()
    return jsonify({"status": "success", "application": application.serialize()}), 200


@bp_application.route('/applications/<int:application_id>', methods=['DELETE']) #el aplicante puede eliminar su aplicacion  delete 
@jwt_required()
def delete_application(application_id):
    user_id = get_jwt_identity()
    application = Application.query.get_or_404(application_id)

    if application.user_id != user_id:
        return jsonify({"status": "error", "message": "Not authorized"}), 403
    
    application.delete()
    return jsonify({"status": "success", "message": "Application deleted"}), 200