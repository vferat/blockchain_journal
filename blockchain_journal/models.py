from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager
 
login = LoginManager()
db = SQLAlchemy()


written_papers = db.Table('Written_papers',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('paper_id', db.Integer, db.ForeignKey('papers.id'), primary_key=True)
)

class UserModel(UserMixin, db.Model):
    __tablename__ = 'users'
 
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80), unique=True)
    username = db.Column(db.String(100))
    password_hash = db.Column(db.String())

    tokens = db.Column(db.Float, default='10')
    locked_tokens = db.Column(db.Float, default='0')    
 
    def set_password(self,password):
        self.password_hash = generate_password_hash(password)
     
    def check_password(self,password):
        return check_password_hash(self.password_hash,password)

    papers = db.relationship('PaperModel', secondary=written_papers, lazy='subquery',
                                backref=db.backref('PaperModel', lazy=True))

class PaperModel(db.Model):
    __tablename__ = 'papers'
 
    id = db.Column(db.Integer, primary_key=True)
    doi = db.Column(db.String(100))


