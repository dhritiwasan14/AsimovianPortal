from flask import Flask 
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_mail import Mail
from mailer import Mailer

import config

app = Flask(__name__)
app.config.from_object(config.DevConfig)
app.secret_key = config.Config.SECRET_KEY

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
mail = Mail(app)

mailer = Mailer(mail)

import routes, models

migrate = Migrate(app, db)

models.Group.query.order_by(models.Group.username).all()

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(id):
	print(id)
	group = models.Group.query.get(int(id))
	return group