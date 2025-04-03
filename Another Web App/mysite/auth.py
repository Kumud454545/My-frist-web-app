from . import db
from .models import User
from flask import Blueprint, render_template, request, url_for, flash, redirect
from flask_login import current_user, login_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint('auth',__name__)

@auth.route('/sign_up',methods=["GET","POST"])
def sign_up():
	if request.method == "POST":
		username = request.form.get('username')
		email = request.form.get('email')
		p1 = request.form.get('password1')
		p2 = request.form.get('password2')
		user = User.query.filter_by(email=email).first()
		if user:
			flash("Account Already Exists",category="error")
			pass
		if not username:
			flash("You gotta have a username",category="error")
			print('1')
			pass
		elif len(email)<4:
			flash("Enter your full email dude", category="error")
			print('2')
			pass
		elif len(p1)<6:
			flash("Whats that supposed to be? Not a password, thats for sure. Make it longer", category="error")
			print('3')
			pass
		elif p1 != p2:
			flash("Passwords dont match", category="error")
			print('4')
			pass
		else:
			new_user = User(email=email,username=username, password=generate_password_hash(p2,method="pbkdf2:sha256"))
			db.session.add(new_user)
			try:
				db.session.commit()
				login_user(new_user,remember=True)
				print("sucess")
				flash("Account created! Going to the home page.",category="works")
				return redirect(url_for('road.home'))
			except Exception as e:
				#flash(f"There was an error registering your account! {str(e)}",category="error")
				print(e)
	return render_template('sign_up.html',user=current_user)

@auth.route('/login', methods=["GET","POST"])
def login():
	if request.method == "POST":
		email = request.form.get('email')
		user = User.query.filter_by(email=email).first()
		if user:
			password = request.form.get('password')
			cur_pas = user.password
			if check_password_hash(cur_pas,password):
				login_user(user,remember=True)
				print("suc")
				return redirect(url_for('road.home'))
			else:
				flash("Wrong password",category="error")
				print("wp")
		else:
			flash("Account Does Not Exist! Please SignUp for a new account",category="error")
			print("dne")
	return render_template('login.html',user=current_user)

@login_required
@auth.route('/logout')
def logout():
	logout_user()
	return redirect(url_for('auth.login'))