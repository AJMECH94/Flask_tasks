from flask import request
from database import UserModel
from flask_restful import Resource
from flask_jwt_extended import create_access_token
import datetime
from mongoengine.errors import FieldDoesNotExist, NotUniqueError, DoesNotExist
from resources.errors import SchemaValidationError, EmailAlreadyExistsError, UnauthorizedError, \
    InternalServerError


class SignupApi(Resource):

    def post(self):
        try:
            body = request.get_json()
            print(body)
            user = UserModel(**body)
            user.hash_password()
            user.save()
            id = user.id
            return {'id': "user created"}, 200
        except FieldDoesNotExist:
            raise SchemaValidationError
        except NotUniqueError:
            print(EmailAlreadyExistsError)
            raise EmailAlreadyExistsError
        except Exception:
            raise InternalServerError


class LoginApi(Resource):
    def post(self):
        try:
            body = request.get_json()
            user = User.objects.get(email=body.get('email'))
            authorized = user.check_password(body.get('password'))
            if not authorized:
                return {'error': 'Email or password invalid'}, 401
            expires = datetime.timedelta(days=7)
            access_token = create_access_token(identity=str(user.id), expires_delta=expires)
            return {'token': access_token}, 200
        except (UnauthorizedError, DoesNotExist):
            raise UnauthorizedError
        except Exception:
            raise InternalServerError