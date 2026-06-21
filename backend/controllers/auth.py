from flask_restful import Resource
from flask import request, jsonify, make_response
from controllers.models import *
from flask_login import login_user

class Login(Resource):
    def post(self):
        login_credentials = request.get_json()

        # data validation
        if not login_credentials:
            result = {
                'message' : 'Login credentials are requried'
            }

            return make_response(jsonify(result),400)
        email = login_credentials.get('email',None)
        password = login_credentials.get('password',None)

        if not email or not password:
            result = {
                'message' : 'Email and Password are required'
            }
            return make_response(result,400)
        user = User.query.filter_by(email = email).first()


        if not user:
            result = {
                'message' : 'User not found'
            }

            return make_response(result, 404)
        
        if not check_password_hash(user.password,password):
            result = {
                'message' : 'Invalid credentials. Please try again'
            }

            return make_response(result,400)
        
        login_user(user)

        result = {
            'message' : 'Logged in successfully',
            'user' : {
                'id' : user.id,
                'username' : user.username,
                'email' : user.email,
                'role' : user.role
            }
        }

        return make_response(result,201)

