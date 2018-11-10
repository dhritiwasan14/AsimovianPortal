from flask import Flask 
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

import config

app = Flask(__name__)
app.config.from_object(config.DevConfig)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)

import routes, models

models.Group.query.order_by(models.Group.username).all()

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(username):
    group = models.Group.query.filter(username=username).first()
    return group