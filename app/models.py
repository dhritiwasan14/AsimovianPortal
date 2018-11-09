from . import app, db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), unique=True, nullable=False)
    posts = db.relationship('Post', backref='user', lazy=True)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(20), unique=True, nullable=True)
    last_update = db.Column(db.DateTime, nullable=True)
    group = db.Column(db.String, db.ForeignKey('user.username'), nullable=True)
