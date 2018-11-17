import os

_basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = "mysecretkey"
    TEMPLATE_FOLDER = "templates"

    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USERNAME = 'asimovianportal@gmail.com'
    MAIL_PASSWORD = 'Sutd1234'
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False

class DevConfig(object):
    DEBUG = True
    RELOAD = True
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://asimov:asimov@devostrum.no-ip.info/asimov"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USERNAME = 'asimovianportal@gmail.com'
    MAIL_PASSWORD = 'Sutd1234'
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False