import csv

from . import db, app, bcrypt, mail, mailer
from models import Group, Page, Class
from flask import render_template, request, redirect, flash, jsonify
from flask_login import login_user, login_required, logout_user, current_user
import hashlib
import json
import random
import string
from werkzeug import secure_filename

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    from datetime import datetime

    if request.method == 'GET':
	    return render_template('login.html', year = datetime.now().year)
    print('here')
    username = request.form.get('username')
    password = request.form.get('password')

    group = Group.query.filter_by(username=username).first()
    print('failed to connect?')
    if group:
        if bcrypt.check_password_hash(group.password_hash, password):
            login_user(group)
            return redirect('/dashboard')

    flash('Invalid username or password')
    return render_template('login.html', year = datetime.now().year)

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


@app.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return redirect('/')

@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def admin_dashboard():
    group = Group.query.get(int(current_user.get_id()))
    if group.is_admin():
        classes = Class.query.all()
        return render_template('admin-dashboard.html', username = "admin", usernameHash = hashlib.md5("admin"), classes=classes)
    else:
        return redirect('/student-dashboard/' + group.username)

@app.route('/dashboard/add-groups', methods=['POST'])
def add_groups():
    group_file = request.files['group-file']

    groups = []

    filename = group_file.filename
    if filename.split('.')[-1] == 'csv': # over here, test again with an actual csv file!!!! 
        csv_reader = csv.reader(group_file, delimiter=',')
        for i, row in enumerate(csv_reader):
            if i > 0:
                group_name, group_members = row[0], row[1:]
                group_members = [v for v in group_members if v != '']

                if group_name == "":
                    continue

                group = dict()
                group['username'] = group_name
                group['members'] = ", ".join(group_members)
                print(group['members'])
                groups.append(group)

    return jsonify(groups)

@app.route('/dashboard/create-class', methods=['POST'])
def create_class():
    class_name = request.form.get('class_name')
    deadline = request.form.get('deadline')
    groups = json.loads(request.form.get('groupJSON'))
    class_create = Class(class_name, deadline)

    print(class_name, deadline, groups)
    db.session.add(class_create)
    db.session.commit()

    for i, g in enumerate(groups):
        group_password = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(8))
        password_hash = bcrypt.generate_password_hash(group_password)
        group = Group(username = g['username'], password_hash=password_hash, members=g['members'], class_id = class_create.id)
        groups[i]['password'] = group_password

        db.session.add(group)

    db.session.commit()
    
    mailer.send_passwords(groups)

    response = dict()

    response['success'] = True
    response['message'] = "Successfully created class " + class_name + "!"

    return jsonify(response)

@app.route('/student-dashboard/<username>', methods=['GET'])
@login_required
def student_dashboard(username):
    # add post, redirect to 
    # click existing post, 
    group = Group.query.get(int(current_user.get_id()))
    if group.is_admin() or group.username == username:
        return render_template('student-dashboard.html', username = username, usernameHash = hashlib.md5(username))
    else:
        return redirect('/student-dashboard/' + group.username)

# @app.route('/student-editor/<username>/<page>', methods=['GET', 'POST'])
# @login_required
# def student_editor(username, page):
#     # handle post request for image upload, save as draft, prompt save. 
#     image = request.form.get('')