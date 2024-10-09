import os
import cloudinary
from flask import Flask, request, jsonify
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from models import db
from dotenv import load_dotenv
from routes.auth import bp_auth
from routes.profile import bp_profile
from routes.applications import bp_application
from routes.languages import bp_languages
from routes.ranks import bp_ranks
from routes.status import bp_status
from routes.technologies import bp_technologies
from routes.job_postings import bp_job_posting
from routes.PostLanguage import bp_post_language
from routes.rankingApplications import bp_rankingApplications
from routes.rankingJobPosting import bp_rankingJobPosting
from routes.techKnowledge import bp_tech_knowledge


load_dotenv()

cloudinary.config( 
  cloud_name = os.getenv('CLOUDINARY_CLOUD_NAME'), 
  api_key = os.getenv('CLOUDINARY_CLOUD_API_KEY'), 
  api_secret = os.getenv('CLOUDINARY_CLOUD_API_SECRET'),
  secure = True
)

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_TRACKS_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')

db.init_app(app)
Migrate(app, db)
jwt = JWTManager(app)
CORS(app)

app.register_blueprint(bp_auth, url_prefix="/api")
app.register_blueprint(bp_profile, url_prefix="/api")
app.register_blueprint(bp_application, url_prefix="/api")
app.register_blueprint(bp_languages, url_prefix="/api")
app.register_blueprint(bp_ranks, url_prefix="/api")
app.register_blueprint(bp_status, url_prefix="/api")
app.register_blueprint(bp_technologies, url_prefix="/api")
app.register_blueprint(bp_job_posting, url_prefix="/api")
app.register_blueprint(bp_post_language, url_prefix="/api")
app.register_blueprint(bp_rankingApplications, url_prefix="/api")
app.register_blueprint(bp_rankingJobPosting, url_prefix="/api")
app.register_blueprint(bp_tech_knowledge, url_prefix="/api")


@app.route('/')
def main():
    return jsonify({"message": "Server running successfully!"}), 200

if __name__ == '__main__':
    app.run()
