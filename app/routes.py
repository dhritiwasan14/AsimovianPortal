import csv, os, base64
import uuid 

from . import db, app, bcrypt, mailer
from models import Group, Page, Class
from flask import render_template, request, redirect, flash, jsonify, send_from_directory
from flask_login import login_user, login_required, logout_user, current_user
import hashlib
import json
import random
import string
import datetime
import mistune
from werkzeug import secure_filename


from helper import markdown_to_text

BASE_DIR =  os.getcwd()
UPLOADS_DIR = BASE_DIR + '/app/uploads/'
POSTS_FOLDER = BASE_DIR + '/app/posts/'
app.config['UPLOADS_FOLDER'] = UPLOADS_DIR
app.config['POSTS_FOLDER'] = POSTS_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    from datetime import datetime

    if request.method == 'GET':
	    return render_template('login.html', year = datetime.now().year)
    username = request.form.get('username')
    password = request.form.get('password')

    group = Group.query.filter_by(username=username).first()
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
        return render_template('admin-dashboard.html', username = "admin", usernameHash = hashlib.md5("admin").hexdigest(), classes=classes)
    else:
        return redirect('/student-dashboard/' + group.username)

@app.route('/dashboard/add-groups', methods=['POST'])
@login_required
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

@app.route('/dashboard/reset-group-password', methods=['POST'])
@login_required
def reset_group_password():
    username = request.form.get('username')
    group = db.session.query(Group).filter_by(username = username)[0]

    group_password = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(8))
    group.password_hash = bcrypt.generate_password_hash(group_password)

    g = dict()
    g['username'] = username
    g['members'] = group.members
    g['password'] = group_password

    mailer.send_passwords([g])

    db.session.commit()

    response = dict()
    response['success'] = True

    return jsonify(response)

@app.route('/dashboard/get-classes', methods=['GET'])
@login_required
def get_classes():
    result = Class.query.all()

    classes = []
    for c in result:
        cls = dict()
        cls['id'] = c.id
        cls['name'] = c.class_name
        cls['deadline'] = str(c.deadline)
        cls['groupcount'] = Group.query.filter_by(class_id = c.id).count()
        classes.append(cls)

    response = dict()
    response['classes'] = classes
    response['success'] = True

    return jsonify(response)

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

@app.route('/dashboard/delete-class', methods=['POST'])
@login_required
def delete_class():
    id = request.form.get('id')

    Group.query.filter_by(class_id = id).delete()
    Class.query.filter_by(id=int(id)).delete()

    db.session.commit()

    response = dict()
    response['success'] = True

    return jsonify(response)

@app.route('/dashboard/get-class/<id>', methods=['GET'])
@login_required
def get_class(id):
    cls = Class.query.get(int(id))
    groups = db.session.query(Group).filter_by(class_id=id)

    response = dict()
    response['success'] = True
    response['class'] = dict()
    response['class']['name'] = cls.class_name
    response['class']['deadline'] = str(cls.deadline)
    response['class']['groups'] = []

    for g in groups:
        group = dict()
        group['username'] = g.username
        group['members'] = g.members
        response['class']['groups'].append(group)

    return jsonify(response)

@app.route('/student-dashboard/<username>', methods=['GET'])
@login_required
def student_dashboard(username):
    # add post, redirect to 
    # click existing post, 
    # need to send each post for the user.
    group = Group.query.get(int(current_user.get_id())) # because of this, might not be possible to redirect admin

    pages = Page.query.filter_by(group_id=group.id).all()
    if group.is_admin() or group.username == username:
        images, titles = [], []
        if not os.path.isdir(UPLOADS_DIR+username):
            os.mkdir(UPLOADS_DIR+username)
        list_files = os.listdir(UPLOADS_DIR+username)
        for entry in list_files:
            images.append('/uploads/'+username+'/'+entry)
        return render_template('student-dashboard.html', username = username, usernameHash = hashlib.md5(username).hexdigest(), images=images)
    else:
        return redirect('/login')

@app.route('/student-dashboard/<username>/get-pages', methods=['GET'])
@login_required
def get_pages(username):
    group = Group.query.filter_by(username=username)[0]
    pageResult = Page.query.filter_by(group_id=group.id)

    pages = []

    for p in pageResult:
        page = dict()
        page['name'] = p.name
        page['id'] = p.id
        page['last_update'] = p.last_update
        page['is_main'] = p.is_main

        pages.append(page)

    response = dict()
    response['success'] = True
    response['pages'] = pages
    
    return jsonify(response)

@app.route('/student-dashboard/<username>/get-page/<id>', methods=['GET'])
@login_required
def get_page(username, id):
    pageResult = Page.query.get(int(id))

    page = dict()
    page['name'] = pageResult.name

    pageFile = open(POSTS_FOLDER + username + "/" + str(pageResult.id) + ".txt", "r")
    pageContent = ""

    for l in pageFile.readlines():
        pageContent += l

    page['content'] = pageContent

    response = dict()
    response['success'] = True
    response['page'] = page

    return jsonify(response)

@app.route('/student-dashboard/<username>/swap-main', methods=['POST'])
@login_required
def swap_main(username):
    first = int(request.form.get('first'))
    second = int(request.form.get('second'))

    if first != 0:
        firstPage = Page.query.get(first)
        firstPage.is_main = 0

    secondPage = Page.query.get(second)
    secondPage.is_main = 1

    db.session.commit()

    response = dict()
    response['success'] = True

    return jsonify(response)
# @app.route('/student-editor/<username>/<page>', methods=['GET', 'POST'])
# @login_required
# def student_editor(username, page):
#     # handle post request for image upload, save as draft, prompt save. 
#     image = request.form.get('')


@app.route('/upload-image/<username>', methods=['POST'])
@login_required
def upload_image(username):
    file_image = request.files['image']
    file_name = uuid.uuid4().hex[:6].upper()
    # check if dir exists else create
    
    if not os.path.isdir(UPLOADS_DIR+username):
        os.mkdir(UPLOADS_DIR+username)
    file_image.save(UPLOADS_DIR+username+'/'+file_name+'.'+file_image.filename.split('.')[-1])
    return '/uploads/'+username+'/'+file_name+'.'+file_image.filename.split('.')[-1]


@app.route('/uploads/<username>/<filename>', methods=['GET'])
@login_required
def get_img_link(username, filename):
    return send_from_directory(app.config['UPLOADS_FOLDER']+username+'/', filename, as_attachment=True)


@app.route('/wiki', methods=['GET'])
def wiki(username):
    group = Group.query.get(int(current_user.get_id())) # because of this, might not be possible to redirect admin

    
    # if group.is_admin() or group.username == username:
    #     pageResult = Page.query.filter_by(group_id=group.id)

    #     pages = []

    #     for p in pageResult:
    #         page = dict()
    #         page['name'] = p.name
    #         page['id'] = p.id
    #         page['last_update'] = p.last_update.strftime('%m/%d/%Y')
    #         page['is_main'] = p.is_main
    #         f = open(POSTS_FOLDER+username+'/'+str(p.id)+'.txt')
    #         page['description'] = markdown_to_text(f.read())[:300]
    #         f.close()
    #         pages.append(page)
        
    #     response = dict()
    #     response['success'] = True
    #     response['pages'] = pages
    #     return render_template('wiki.html', response=response, username=username)
    return redirect('/login')



@app.route('/wiki/<username>', methods=['GET'])
def wiki_page(username):
    group = Group.query.get(int(current_user.get_id())) # because of this, might not be possible to redirect admin

    
    if group.is_admin() or group.username == username:
        p = Page.query.filter_by(group_id=group.id, is_main=True).first()
        page = dict()
        page['name'] = p.name
        page['id'] = p.id
        page['last_update'] = p.last_update.strftime('%m/%d/%Y')
        f = open(POSTS_FOLDER+username+'/'+str(p.id)+'.txt')
        renderer = mistune.Renderer(escape=False)
        markdown = mistune.Markdown(renderer=renderer)
        page['content'] = markdown(f.read())
        f.close()
        
        response = dict()
        response['success'] = True
        response['main_page'] = page


        return render_template('wiki-page.html', response=response, username=username)
    return redirect('/login')

@app.route('/student-dashboard/<username>/add-page', methods=["POST"])
@login_required
def add_page(username):
    title = request.form.get('title')
    post = request.form.get('content')
    group = db.session.query(Group).filter_by(username=username).first()
    page = Page(datetime.datetime.now(), group.id, name=title)
    db.session.add(page)
    db.session.commit()
    if not os.path.isdir(POSTS_FOLDER+username):
        os.mkdir(POSTS_FOLDER+username)

    f = open(POSTS_FOLDER+username+'/'+str(page.id)+'.txt', 'w')
    f.write(post)
    f.close()

    response = dict()
    response['success'] = True

    return jsonify(response)

@app.route('/student-dashboard/<username>/delete-page', methods=["POST"])
@login_required
def delete_page(username):
    id = request.form.get('id')
    Page.query.filter_by(id=int(id)).delete()
    db.session.commit()
    if os.path.exists(POSTS_FOLDER + username + "/" + id + ".txt"):
        os.remove(POSTS_FOLDER + username + "/" + id + ".txt")

    response = dict()
    response['success'] = True

    return jsonify(response)

@app.route('/student-dashboard/<username>/edit-page', methods=["POST"])
@login_required
def edit_page(username):
    title = request.form.get('title')
    post = request.form.get('content')
    id = request.form.get('id')

    page = Page.query.get(int(id))
    page.name = title
    db.session.commit()

    if not os.path.isdir(POSTS_FOLDER+username):
        os.mkdir(POSTS_FOLDER+username)

    f = open(POSTS_FOLDER+username+'/'+str(page.id)+'.txt', 'w')
    f.write(post)
    f.close()

    response = dict()
    response['success'] = True

    return jsonify(response)
