from . import app, db

class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    salt = db.Column(db.String(256), nullable=False)
    pages = db.relationship('Page', backref='user', lazy=True)

class Page(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    last_update = db.Column(db.DateTime, nullable=True)
    group = db.Column(db.Integer, db.ForeignKey('group.id'), nullable=True)
