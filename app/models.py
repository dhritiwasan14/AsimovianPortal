from . import app, db, bcrypt

from flask_login import UserMixin

class Group(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    admin = db.Column(db.Integer, default=0, nullable=False)
    pages = db.relationship('Page', backref='user', lazy=True)
    # authenticated = db.Column(db.Boolean, default=False)

    def __init__(self, username, password):
        self.username = username
        self.password_hash = password
 
    # def is_authenticated(self):
    #     return self.authenticated
 
    def is_active(self):
        return True
 
    def is_anonymous(self):
        return False
 
    def get_id(self):
        return unicode(self.id)

    def is_admin(self):
        return self.is_admin
 
    def __repr__(self):
        return '<Group %r>' % (self.username)


class Page(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    last_update = db.Column(db.DateTime, nullable=True)
    group = db.Column(db.Integer, db.ForeignKey('group.id'), nullable=True)
