from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    
    
    profile = db.relationship('Profile', backref="user", uselist=False)
    job_postings = db.relationship('JobPosting', backref="user", lazy=True)
    applications = db.relationship('Application', backref="user", lazy=True)
    RankingJobPosting = db.relationship('RankingJobPosting', backref="user", lazy=True)
    RankingApplications = db.relationship('RankingApplications', backref="user", lazy=True)



    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "is_active": self.is_active,
            "profile": self.profile.serialize() if self.profile else None
        }

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()



class Profile(db.Model):
    __tablename__ = 'profiles'
    id = db.Column(db.Integer, primary_key=True)
    biography = db.Column(db.String, default="")
    github = db.Column(db.String, default="")
    linkedin = db.Column(db.String, default="")
    avatar = db.Column(db.String, default="")
    public_id = db.Column(db.String, default="")
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "biography": self.biography,
            "github": self.github,
            "linkedin": self.linkedin,
            "avatar": self.avatar
        }

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()



class JobPosting(db.Model):
    __tablename__ = 'job_postings'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    payment = db.Column(db.Float, nullable=False)
    date = db.Column(db.DateTime, default=datetime.now)
    required_time = db.Column(db.Integer, nullable=False)
    expiration_date = db.Column(db.DateTime, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    
    applications = db.relationship('Application', backref='job_posting', lazy=True)
    post_languages = db.relationship('PostLanguage', backref='job_posting', lazy=True)  
    tech_knowledges = db.relationship('TechKnowledge', backref='job_posting', lazy=True)  
    RankingJobPosting = db.relationship('RankingJobPosting', backref="job_posting", lazy=True)

    def serialize(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "payment": self.payment,
            "employer": self.user_id,
            "date": self.date,
            "required_time": self.required_time,
            "expiration_date": self.expiration_date
        }

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class PostLanguage(db.Model):
    __tablename__ = 'post_languages'

    job_posting_id = db.Column(db.Integer, db.ForeignKey('job_postings.id'), nullable=False, primary_key=True)
    language_id = db.Column(db.Integer, db.ForeignKey('languages.id'), nullable=False, primary_key=True)


    language = db.relationship('Language', backref='post_languages')

    def serialize(self):
        return {
            "job_posting_id": self.job_posting_id,
            "language": self.language_id
        }


class TechKnowledge(db.Model):
    __tablename__ = 'tech_knowledges'
    id = db.Column(db.Integer, primary_key=True)
    job_posting_id = db.Column(db.Integer, db.ForeignKey('job_postings.id'), nullable=False)
    rank_id = db.Column(db.Integer, db.ForeignKey('ranks.id'), nullable=False)
    technologies_id = db.Column(db.Integer, db.ForeignKey('technologies.id'), nullable=False)


    Technologies = db.relationship('Technologies', backref='tech_knowledges')
    rank = db.relationship('Rank', backref='tech_knowledges')

    def serialize(self):
        return {
            "id": self.id,
            "job_posting_id": self.job_posting_id,
            "rank": self.rank_id,
            "technologies": self.technologies_id
        }


class RankingJobPosting(db.Model):
    __tablename__ = 'RankingJobPosting'
    id =  db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    ranking = db.Column(db.Integer, nullable=False)
    jobPosting_id = db.Column(db.Integer, db.ForeignKey('job_postings.id'), nullable=False)

    job_postings = db.relationship('JobPosting', backref='RankingJobPosting')

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "ranking": self.ranking,
            "jobPosting_id": self.jobPosting_id
        }


class RankingApplications(db.Model):
    __tablename__ = 'RankingApplication'
    id =  db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    ranking = db.Column(db.Integer, nullable=False)
    application_id = db.Column(db.Integer, db.ForeignKey('applications.id'), nullable=False)

    Application = db.relationship('Application', backref='RankingApplication')


    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "ranking": self.ranking,
            "application_id": self.application_id
        }


class Status(db.Model):
    __tablename__ = 'status'
    id =  db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)


    def serialize(self):
        return {
            "id": self.id,
            "name": self.name
        }


class Rank(db.Model):
    __tablename__ = 'ranks'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name
        }



class Language(db.Model):
    __tablename__ = 'languages'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name
        }


class Technologies(db.Model):
    __tablename__ = 'technologies'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name
        }

class Application(db.Model):
    __tablename__ = 'applications'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    job_posting_id = db.Column(db.Integer, db.ForeignKey('job_postings.id'), nullable=False)
    status_id = db.Column(db.Integer, db.ForeignKey('status.id'), nullable=False)
    date = db.Column(db.DateTime, default=datetime.now)

    status = db.relationship('Status', backref='applications')

    def serialize(self):
        return {
            "id": self.id,
            "user": self.user_id,
            "job": self.job_posting_id,
            "status": self.status_id,
            "date": self.date
        }

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
