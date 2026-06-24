from controllers.database import db
from controllers.models import *
from flask_restful import Resource
from flask import request, jsonify, make_response
from flask_jwt_extended import jwt_required, get_jwt_identity

class Company(Resource):
    @jwt_required
    def get(self):
        pass
    @jwt_required()
    def post(self):
        user_id = get_jwt_identity()

        user = User.query.get(user_id)

        if user.role != "company":
            return {"message": "Access denied"}, 403

        # create company profile
    @jwt_required
    def put(self):
        pass

