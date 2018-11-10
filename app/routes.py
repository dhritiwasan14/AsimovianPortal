from . import db, app, bcrypt
from models import Group, Page

from flask import render_template, request, redirect, flash
from flask_login import login_user, login_required, logout_user, current_user


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    from datetime import datetime
    print(request.form.get('password'))
    if request.method == 'GET':
	    return render_template('login.html', year = datetime.now().year)
    username = request.form.get('username')
    password = request.form.get('password')

    group = Group.query.filter_by(username=username).first()
    
    if group:
        if bcrypt.check_password_hash(group['password'], password):

            login_user(group)
            flask.flash('Login Successful')
            return redirect('/'+group['username'])
    flash('Invalid username or password')
    return render_template('login.html', year = datetime.now().year)

@app.route('/<username>', methods=['GET'])
def group_dashboard(username):
    return render_template('index.html')

@app.route('/register', methods=['GET'])
def register():
    ''' Create admin account if it does not exist '''
    from datetime import datetime

    exists = db.session.query(Group.id).filter_by(username='admin').scalar() is not None

    if not exists:
        username = 'admin'
        password = 'password'
        password_hash = bcrypt.generate_password_hash(password)
        admin = 1

        group = Group(username, password_hash, admin)

        db.session.add(group)
        db.session.commit()

        message = "Admin account successfully created!"
    else:
        message = "Admin account exists already!"

    return render_template('register.html', message = message, year = datetime.now().year)
    # if request.method == 'GET':
    #     return render_template('register.html')
    # username = request.form.get('username')
    # password = request.form.get('password')
    # pw_hash = bcrypt.generate_password_hash(password)
    # group = Group(username=username, password_hash=pw_hash)
    # db.session.add(group)
    # db.session.commit()
    # flash('Sign up successful.')
    # return render_template('register.html')
