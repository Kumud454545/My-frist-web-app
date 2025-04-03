from flask import Blueprint, redirect, url_for, render_template, request
from flask_login import login_required, current_user
from . import db
from .models import Message, User
from sqlalchemy import asc

road = Blueprint('road',__name__)

@login_required
@road.route('/home',methods=["GET","POST"])
def home():
	if request.method == "POST":
		content = request.form.get('message')
		if content != None and len(content)>0:
			userid = current_user.id
			new_message = Message(userid=userid,content=content)
			db.session.add(new_message)
			db.session.commit()
			print("Message sent")
		else:
			print("Not sent")
	all_messages = Message.query.order_by(asc(Message.date)).all()
	print(all_messages)
	if current_user.is_authenticated:
		return render_template('home.html',user=current_user,messages=all_messages)
	else:
		return redirect(url_for("auth.sign_up"))

@login_required
@road.route('/')
def redir_home():
	if current_user.is_authenticated:
		return redirect(url_for("road.home"))
	else:
		return redirect(url_for("auth.sign_up"))