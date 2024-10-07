from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, unique=True, nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    profile = db.relationship('Profile', backref="user", uselist=False)

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "is_active": self.is_active,
            "profile": self.profile.serialize()
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
    users_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

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
    location = db.Column(db.String, nullable=False)
    salary = db.Column(db.Float, nullable=True)
    employer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  
    applications = db.relationship('Application', backref='job', lazy=True)  

    def serialize(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "location": self.location,
            "salary": self.salary,
            "employer": self.employer_id
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

    status = db.Column(db.String, default="pending")  

    def serialize(self):
        return {
            "id": self.id,
            "user": self.applicant.email,  
            "job": self.job.title,  
            "status": self.status
        }

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()