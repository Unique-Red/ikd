from website import db
from sqlalchemy.sql import func
from flask_login import UserMixin

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(20), nullable=False)
    text = db.Column(db.String(200), nullable=False)
    file = db.Column(db.String(150), nullable=False)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(30), nullable=False)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())