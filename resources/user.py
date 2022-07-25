from flask_restful import Resource, reqparse
from models.user import UserModel

class User(Resource):

    def get(self, user_id):
        user = UserModel.find_user(user_id)
        if user:
            return user.json()
        return {'message': 'User not found.'}, 404 #Not found alert

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
        attributes = reqparse.RequestParser()
        attributes.add_argument('login', type=str, required=True, help="The field 'login' cannot be left blank.")
        attributes.add_argument('password', type=str, required=True, help="The field 'password' cannot be left blank.")
        data = attributes.parse_args()

        if UserModel.find_by_login(data['login']):
            return {"message": "The login '{}' already exist.".format(data['login'])}

        user = UserModel(**data)
        user.save_user()
        return {'message': 'User created successfully.'}, 201 #Created