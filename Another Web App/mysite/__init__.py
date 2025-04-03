from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user
from os import path

db = SQLAlchemy()
DBNAME="database.db"

def create_app():
	app = Flask(__name__)
	app.config["SECRET_KEY"] = "gsdjbhcavghh xyz"
	app.config["SQLALCHEMY_DATABASE_URI"] = f'sqlite:///{DBNAME}'
	db.init_app(app)

	from .roads import road
	from .auth import auth

	app.register_blueprint(road)
	app.register_blueprint(auth)

	from .models import User, Message

	create_database(app)

	login_manager = LoginManager()
	login_manager.login_view = 'auth.login'
	login_manager.init_app(app)

	@login_manager.user_loader
	def load_user(user_id):
		return User.query.get(user_id)

	return app

def create_database(app):
	if not path.exists('instance/' + DBNAME):
		with app.app_context():
			db.create_all()
			print("Database Created!")