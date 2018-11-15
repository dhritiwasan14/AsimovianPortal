import csv

from . import db, app, bcrypt
from models import Group, Page, Class

from flask import render_template, request, redirect, flash
from flask_login import login_user, login_required, logout_user, current_user
import hashlib
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
def admin_dashboard():
    if request.method == 'POST':
        class_name = request.form.get('class-name')
        deadline = request.form.get('deadline')
        f = request.files['file']
        filename = f.filename
        class_create = Class(class_name, deadline)
        db.session.add(class_create)
        if filename.split('.')[1] == 'csv': # over here, test again with an actual csv file!!!! 
            csv_reader = csv.reader(f, delimiter=',')
            line_count = 0
            for row in csv_reader:
                if line_count > 0:
                    group_username, group_password, group_members = row[0], row[1], row[2:]
                    password_hash = bcrypt.generate_password_hash(group_password)
                    group = Group(username=group_username, password=password_hash, members=', '.join(members), class_id=class_create.id)
                    db.session.add(group)
                line_count += 1

        db.session.commit()
        flash('Successfully created a class. ')
    group = Group.query.get(int(current_user.get_id()))
    if group.is_admin():
        return render_template('admin-dashboard.html', username = "admin", usernameHash = hashlib.md5("admin"))
    else:
        return redirect('/student-dashboard/' + group.username)

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