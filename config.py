import os

# Flask app settings
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI ='sqlite:///' + os.path.join(basedir, 'database.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = 'you-will-never-guess'

UPLOAD_FOLDER = os.path.join(basedir, 'app/static/uploads')