# Imports
from . import db, bcrypt
from marshmallow import fields, Schema, validate
import datetime


class UserModel(db.Model):
    '''
    ORM to manage Users
    '''

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    username = db.Column(db.String(128), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __init__(self, data):
        """
        Class constructor
        """
        self.name = data.get('name')
        self.username = data.get('username')
        self.password = self.__generate_hash(data.get('password'))
        self.created_at = datetime.datetime.utcnow()
        self.role = data.get('role')

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def get_one_user(id):
        return UserModel.query.get(id)

    @staticmethod
    def get_user_by_username(value):
        return UserModel.query.filter_by(username=value).first()

    def __generate_hash(self, password):
        return bcrypt.generate_password_hash(password, rounds=10).decode("utf-8")

    def check_hash(self, password):
        return bcrypt.check_password_hash(self.password, password)

    def __repr(self):
        return '<id {}>'.format(self.id)


# Schema for serilazitation and validation
class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Regexp(regex=r'^[a-zA-Z ]{1,}$', error="Name must conatin only alphabets"))
    username = fields.Str(required=True, validate=validate.Length(min=8))
    password = fields.Str(required=True, load_only=True, validate=validate.Regexp(regex=r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{10,}$', error='Passowrd must have one special character, one number, one upper case character, one lower case character and must be atleast 10 characters long'))
    created_at = fields.DateTime(dump_only=True)


class UserLoginSchema(Schema):
    username = fields.Str()
    password = fields.Str()