from . import db
from sqlalchemy.sql import func
from flask_login import UserMixin

class User(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String(255), unique=True)
	username = db.Column(db.String(100))
	password = db.Column(db.String(300))
	messages = db.relationship('Message', back_populates='user', lazy=True)

class Message(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	userid = db.Column(db.Integer, db.ForeignKey('user.id'))
	content = db.Column(db.Text(10000))
	date = db.Column(db.DateTime(timezone=True),default=func.now())
	user = db.relationship('User', back_populates='messages')