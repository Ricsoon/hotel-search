from flask_restful import Resource, reqparse
from blacklist import BLACKLIST
from models.user import UserModel
from flask_jwt_extended import create_access_token, get_jwt, jwt_required, get_jwt
from werkzeug.security import safe_str_cmp

attributes = reqparse.RequestParser()
attributes.add_argument('login', type=str, required=True, help="The field 'login' cannot be left blank.")
attributes.add_argument('password', type=str, required=True, help="The field 'password' cannot be left blank.")

class User(Resource):

    def get(self, user_id):
        user = UserModel.find_user(user_id)
        if user:
            return user.json()
        return {'message': 'User not found.'}, 404 #Not found alert

    @jwt_required()
    def delete(self, user_id):
        user = UserModel.find_user(user_id)
        if user:
            try:
                user.delete_user()
            except:
                return {'message': 'An internal error ocurrred trying to delete user.'}, 500 #Internal Server Error
            return {'message': 'User deleted.'}
        return {'message': 'User not found.'}, 404 #Not Found

class UserRegister(Resource):
    def post(self):
        data = attributes.parse_args()

        if UserModel.find_by_login(data['login']):
            return {"message": "The login '{}' already exist.".format(data['login'])}

        user = UserModel(**data)
        user.save_user()
        return {'message': 'User created successfully.'}, 201 #Created

class UserLogin(Resource):

    @classmethod
    def post(cls):
        data = attributes.parse_args()

        user = UserModel.find_by_login(data['login'])

        if user and safe_str_cmp(user.password, data['password']):
            access_token = create_access_token(identity=user.user_id)
            return {'access_token': access_token}, 200 #Ok
        return {'message': 'The username or password is incorrect.'}, 401 #Unauthorize

class UserLogout(Resource):

    @jwt_required()
    def post(self):
        jwt_id = get_jwt()['jti'] # JWT TOKEN IDENTIFIER
        BLACKLIST.add(jwt_id)
        return {'message': 'Logged out successfully.'}, 200 #Ok