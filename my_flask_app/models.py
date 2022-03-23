from datetime import datetime
from my_flask_app import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(20),unique=True, nullable=False)
    username= db.Column(db.String(120), unique=True, nullable=False) 
    hashed_password=db.Column(db.String(128))


    def __repr__(self):
        return f"User('{self.firstname}','{self.username}')"


    #adated from Grinberg(2014, 2018)
    @property
    def password(self):
         raise AttributeError('Password is not readable.')

    @password.setter
    def password(self,password):
         self.hashed_password=generate_password_hash(password)

    def verify_password(self,password):
        return check_password_hash(self.hashed_password,password)


@login_manager.user_loader
def load_user(user_id):
  return User.query.get(int(user_id))


class Question(db.Model):
    q_id = db.Column(db.Integer, primary_key=True)
    question= db.Column(db.String(300), unique=False, nullable=False)
    option1 = db.Column(db.String(128), unique=False, nullable=False)
    option2= db.Column(db.String(128), unique=False, nullable=False)
    option3 = db.Column(db.String(128), unique=False, nullable=True)
    option4= db.Column(db.String(128), unique=False, nullable=True)
    answer= db.Column(db.String(128), unique=False, nullable=False)
    feedback= db.Column(db.String(300), unique=False, nullable=False)
    level= db.Column(db.String(20),unique=False, nullable=False)
    tag= db.Column(db.String(20),unique=False, nullable=False)