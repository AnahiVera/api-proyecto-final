from flask import Blueprint, request, jsonify
from models import Language, PostLanguage

bp_languages = Blueprint('languages', __name__)

@bp_languages.route('/languages', methods=['GET'])
def get_languages():
    languages = Language.query.all()
    return jsonify({"status": "success", "languages": languages.serialize()}), 200