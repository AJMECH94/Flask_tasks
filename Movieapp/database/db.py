from flask_mongoengine import MongoEngine

""" Here we have imported MongoEngine and created the db object and we have defined a 
function initialize_db() which we are gonna call from our app.py to initialize the 
database."""
db = MongoEngine()


def initialize_db(app):
    db.init_app(app)
