import os

# Settings for development environment
class Development(object):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    DEBUG = True
    TESTING = False
    THREADED = True
    JWT_SECRET_KEY = 'gefgiuwhui7969874u9ihrio7y348yhiuwehoiuf0(*&G*)&'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'host.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


app_config = {
    'development': Development,
}
