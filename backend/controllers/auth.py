from flask_restful import Resource
from flask import request, jsonify, make_response
from controllers.models import *
from flask_jwt_extended import create_access_token
from controllers.database import db
import re


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

        if not (email and password):
            result = {
                'message' : 'Email and Password are required'
            }
            return make_response(result,400)
        user = User.query.filter_by(email = email).first()


        if not user:
            result = {
                'message' : 'Invalid credentials. Please try again'
            }

            return make_response(result, 401)
        
        if not user.active:
            return {'message' : 'Account is inactive'}, 203
        
        if not user.check_password(password):
            result = {
                'message' : 'Invalid credentials. Please try again'
            }

            return make_response(result,401)
        
        token = create_access_token(identity=str(user.id))
        result = {
            'message' : 'Logged in successfully',
            'access_token': token,
            'profile_completed' : user.profile_completed,
            'user' : {
                'id' : user.id,
                'email' : user.email,
                'role' : user.role,
                "profile_completed":user.profile_completed
            }
        }

        return make_response(result,200)

class Register(Resource):
    def post(self):
        register_credentials = request.get_json()

        # data validation for registration
        if not register_credentials:
            result = {
                'message' : 'Please enter your credentials'
            }

            return make_response(jsonify(result),400)
        
        email = register_credentials.get('email',None)
        password = register_credentials.get('password',None)
        role = register_credentials.get('role',None)

        if not (email and password and role):
            result = {
                'message' : 'Missing required fields'
            }
            return make_response(result,400)

        if User.query.filter_by(email=email).first():
            return {
                "message": "User with this email already registered"
            }, 409

        EMAIL_REGEX = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"

        if not re.match(EMAIL_REGEX, email):
            return {"message": "Invalid email format"}, 400
        
        if len(password) < 6:
            return {"message" : "Password must be at least 6 characters long"}, 400
        
        allowed_roles = ['student','company']

        if role not in allowed_roles:
            return {"message" : "Invalid Role"}, 400

        user = User(
            email = email,
            role = role,
            active = True,
        )

        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()

        token = create_access_token(identity=str(user.id))
        result = {
            'message' : 'Registered successfully',
            'access_token': token,
            'profile_completed' : user.profile_completed,
            'user' : {
                'id' : user.id,
                'email' : user.email,
                'role' : user.role,
                "profile_completed":user.profile_completed
            }
        }

        return make_response(result, 201)