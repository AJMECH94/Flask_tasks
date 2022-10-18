from flask import Flask, jsonify
from flask.views import MethodView
from flask_sqlalchemy import SQLAlchemy
from flask import request
from flask_marshmallo import Marshmallo

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"

db = SQLAlchemy(app)
ma = Marshmallo(app)


class Publications(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)

class PublicationsSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Publications



class Stories(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.Text, nullable=True)


class StoriesSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Stories


class StoryCategories(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)


class StoryCategoriesSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = StoryCategories


class UserBookmarks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # title = db.Column(db.String, nullable=False)


class UserBookmarksSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = UserBookmarks


class Podcasts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)


class PodcastsSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Podcasts


class EditorsChoice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # title = db.Column(db.String, nullable=False)


class EditorsChoiceSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = EditorsChoice


class Sections(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # title = db.Column(db.String, nullable=False)


class SectionsSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Sections


class ContentSections(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)


class ContentSectionsSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ContentSections

