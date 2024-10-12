from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()


post_languages = db.Table(
    "post_languages",
    db.Column("job_posting_id", db.Integer, db.ForeignKey('job_postings.id'), nullable=False, primary_key=True),
    db.Column("languages_id", db.Integer, db.ForeignKey('languages.id'), nullable=False, primary_key=True),
)

tech_knowledges = db.Table(
    "tech_knowledges",
    db.Column("job_posting_id", db.Integer, db.ForeignKey('job_postings.id'), nullable=False, primary_key=True),
    db.Column("technologies_id", db.Integer, db.ForeignKey('technologies.id'), nullable=False, primary_key=True)
)

rankingJobPosting = db.Table(
    "rankingJobPosting",
    db.Column("user_id", db.Integer, db.ForeignKey('users.id'), nullable=False, primary_key=True),
    db.Column("ranking_id", db.Integer, db.ForeignKey('ranking.id'), nullable=False),
    db.Column("job_posting_id", db.Integer, db.ForeignKey('job_postings.id'), nullable=False, primary_key=True)
)

rankingApplications = db.Table(
    "rankingApplications",
    db.Column("user_id", db.Integer, db.ForeignKey('users.id'), nullable=False, primary_key=True),
    db.Column("ranking_id", db.Integer, db.ForeignKey('ranking.id'), nullable=False),
    db.Column("application_id", db.Integer, db.ForeignKey('applications.id'), nullable=False, primary_key=True)
)


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
    rank_id = db.Column(db.Integer, db.ForeignKey('ranks.id'), nullable=False)

    applications = db.relationship('Application', backref='job_posting', lazy=True)
    languages = db.relationship('Language', secondary=post_languages, lazy=True)  
    technologies = db.relationship('Technology', secondary=tech_knowledges, lazy=True) 
    ranking = db.relationship('Ranking', secondary=rankingJobPosting, lazy=True)
    

    def serialize(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "payment": self.payment,
            "employer": self.user_id,
            "date": self.date,
            "required_time": self.required_time,
            "expiration_date": self.expiration_date,
            "languages": [lang.name for lang in self.languages],
            "technologies": [tech.name for tech in self.technologies]

        }


    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class Ranking(db.Model):
    __tablename__ = 'ranking'
    id =  db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)


    def serialize(self):
        return {
            "id": self.id,
            "name": self.name
        }
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class Status(db.Model):
    __tablename__ = 'status'
    id =  db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)


    def serialize(self):
        return {
            "id": self.id,
            "name": self.name
        }
    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class Rank(db.Model):
    __tablename__ = 'ranks'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name
        }
    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class Language(db.Model):
    __tablename__ = 'languages'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name
        }
    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class Technology(db.Model):
    __tablename__ = 'technologies'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name
        }
    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

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
