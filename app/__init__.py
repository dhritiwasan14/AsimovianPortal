from flask import Flask 
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

import config

app = Flask(__name__)
app.config.from_object(config.DevConfig)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

import routes, models

models.Group.query.order_by(models.Group.username).all()