import os

_basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = "mysecretkey"
    TEMPLATE_FOLDER = "templates"

class DevConfig(object):
    DEBUG = True
    RELOAD = True
    SQLALCHEMY_DATABASE_URI = "mysql://asimov:asimov@localhost/asimov"
    SQLALCHEMY_TRACK_MODIFICATIONS = False