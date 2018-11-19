from . import app, db, bcrypt

from flask_login import UserMixin

class Group(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    admin = db.Column(db.Integer, default=0, nullable=False)
    pages = db.relationship('Page', backref='user', lazy=True)
    authenticated = db.Column(db.Boolean, default=False)
    members = db.Column(db.String(100), nullable=True)
    class_id = db.Column(db.Integer, db.ForeignKey('class.id'), nullable=False)
    # topic = db.Column(db.Integer, nullable=True, default=0)

    def __init__(self, username, password_hash, class_id, members, admin = 0):
        self.username = username
        self.password_hash = password_hash
        self.admin = admin
        self.members = members
        self.class_id = class_id
 
    def is_authenticated(self):
        #return self.authenticated
        return True
 
    def is_active(self):
        return True
 
    def is_anonymous(self):
        return False
 
    def get_id(self):
        return unicode(self.id)

    def is_admin(self):
        return self.admin
 
    def __repr__(self):
        return '<Group %r>' % (self.username)


class Page(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    last_update = db.Column(db.DateTime, nullable=True)
    group = db.Column(db.Integer, db.ForeignKey('group.id'), nullable=True)
    # main = db.Column(db.Boolean, default=False)
    # name = db.Column(db.String(100), nullable=False)

    def __init__(self, last_update, group, main=False):
        self.last_update = last_update
        self.group = group
        # self.main = main
        # self.name = name

class Class(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    class_name = db.Column(db.String(50), nullable=False)
    deadline = db.Column(db.DateTime, nullable=False)

    def __init__(self, class_name, deadline):
        self.class_name = class_name
        self.deadline = deadline