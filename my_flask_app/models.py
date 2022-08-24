from datetime import datetime
from my_flask_app import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash




class User(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(20),unique=True, nullable=False)
    username= db.Column(db.String(120), unique=True, nullable=False) 
    hashed_password=db.Column(db.String(128))
    dividend_rating= db.Column(db.Integer, unique=False, nullable=True) 
    volatility_rating= db.Column(db.Integer, unique=False, nullable=True) 
    liquidity_rating= db.Column(db.Integer, unique=False, nullable=True) 
    expenses_rating= db.Column(db.Integer, unique=False, nullable=True) 
    user_asset = db.relationship('UserAsset', backref='userasset', lazy=True)
    user_strategy=db.relationship('UserStrategies', backref='userstrategies', lazy=True)


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
    option3 = db.Column(db.String(128), unique=False, nullable=False)
    option4= db.Column(db.String(128), unique=False, nullable=False)

class Strategies(db.Model):
    s_id = db.Column(db.Integer, primary_key=True)
    strategy= db.Column(db.String(300), unique=False, nullable=False)
    bond = db.Column(db.Integer, unique=False, nullable=False)
    stock= db.Column(db.Integer, unique=False, nullable=False)
    commodity = db.Column(db.Integer, unique=False, nullable=False)
    real_estate= db.Column(db.Integer, unique=False, nullable=False)

class Asset(db.Model):
    a_id = db.Column(db.Integer, primary_key=True)
    symbol= db.Column(db.String(128), unique=False, nullable=False)
    etf_name = db.Column(db.String(128), unique=False, nullable=False)
    asset_class= db.Column(db.String(128), unique=False, nullable=False)
    total_assets = db.Column(db.Integer, unique=False, nullable=False)
    avg_volume= db.Column(db.Integer, unique=False, nullable=False)
    etf_database_category= db.Column(db.String(128), unique=False, nullable=False)
    liquidity_rating= db.Column(db.String(128), unique=False, nullable=False)
    expenses_rating= db.Column(db.String(128), unique=False, nullable=False)
    volatility_rating= db.Column(db.String(128), unique=False, nullable=False)
    dividend_rating= db.Column(db.String(128), unique=False, nullable=False)
    

class UserAsset(db.Model):
    u_id = db.Column(db.Integer, primary_key=True)
    symbol= db.Column(db.String(128), unique=False, nullable=False)
    etf_name = db.Column(db.String(128), unique=False, nullable=False)
    asset_class= db.Column(db.String(128), unique=False, nullable=False)
    total_assets = db.Column(db.Integer, unique=False, nullable=False)
    avg_volume= db.Column(db.Integer, unique=False, nullable=False)
    etf_database_category= db.Column(db.String(128), unique=False, nullable=False)
    dividend_rating= db.Column(db.Integer, unique=False, nullable=True) 
    volatility_rating= db.Column(db.Integer, unique=False, nullable=True) 
    liquidity_rating= db.Column(db.Integer, unique=False, nullable=True) 
    expenses_rating= db.Column(db.Integer, unique=False, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class UserStrategies(db.Model):
    us_id = db.Column(db.Integer, primary_key=True)
    strategy= db.Column(db.String(300), unique=False, nullable=False)
    bond = db.Column(db.Integer, unique=False, nullable=False)
    stock= db.Column(db.Integer, unique=False, nullable=False)
    commodity = db.Column(db.Integer, unique=False, nullable=False)
    real_estate= db.Column(db.Integer, unique=False, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)