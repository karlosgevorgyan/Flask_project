import os

basedir = os.path.abspath (os.path.dirname (__file__))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'

    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:1111@localhost/flask_us?charset=utf8mb4'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
