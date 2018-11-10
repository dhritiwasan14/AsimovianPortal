from . import db, app, bcrypt
from models import Group, Page

from flask import render_template, request, redirect, flash
from flask_login import login_user, login_required, logout_user, current_user


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    print(request.form.get('password'))
    if request.method == 'GET':
	    return render_template('login.html')
    username = request.form.get('username')
    password = request.form.get('password')

    group = Group.query.filter_by(username=username).first()
    
    if group:
        if bcrypt.check_password_hash(group['password'], password):

            login_user(group)
            flask.flash('Login Successful')
            return redirect('/'+group['username'])
    flash('Login failed')
    

@app.route('/<username>', methods=['GET'])
def group_dashboard(username):
    return render_template('index.html')

@app.route('/sign_up', methods=['POST', 'GET'])
def sign_up():
    if request.method == 'GET':
        return render_template('signup.html')
    username = request.form.get('username')
    password = request.form.get('password')
    pw_hash = bcrypt.generate_password_hash(password)
    group = Group(username=username, password_hash=pw_hash)
    db.session.add(group)
    db.session.commit()
    flask.flash('Sign up successful.')