from flask import Blueprint, request, jsonify
from models import Language, PostLanguage, db

bp_languages = Blueprint('languages', __name__)

@bp_languages.route('/languages', methods=['GET'])
def get_languages():
    languages = Language.query.all()

    # Serializar cada lenguaje en la lista
    serialized_languages = [language.serialize() for language in languages]

    return jsonify({"status": "success", "languages": serialized_languages}), 200


@bp_languages.route('/languages', methods=['POST'])
def create_language():
    data = request.json
    language_name = data.get('name')

    if not language_name:
        return jsonify({"status": "error", "message": "El nombre del lenguaje es requerido"}), 400

    # Verificar si el lenguaje ya existe
    existing_language = Language.query.filter_by(name=language_name).first()
    if existing_language:
        return jsonify({"status": "error", "message": "El lenguaje ya existe"}), 400

    # Crear un nuevo objeto Language
    new_language = Language(name=language_name)

    try:
        # Insertar en la base de datos
        db.session.add(new_language)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"status": "error", "message": str(e)}), 500

    return jsonify({"status": "success", "language": new_language.serialize()}), 201