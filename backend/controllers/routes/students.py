from controllers.database import db
from controllers.models import *
from flask_restful import Resource
from flask import request, jsonify, make_response
from flask_jwt_extended import jwt_required, get_jwt_identity

class StudentProfile(Resource):
    @jwt_required
    def get(self):
        pass
    @jwt_required()
    def post(self):
        user_id = get_jwt_identity()

        user = User.query.get(user_id)

        if user.role != "student":
            return {"message": "Access denied"}, 403

        # create student profile
        profile_credentials = request.get_json()

        # data validation
        if not profile_credentials:
            result = {
                "message":"Data are requied"
            }
            return make_response(result,400)
        
        full_name = profile_credentials.get('full_name',None)
        roll_number = profile_credentials.get('roll_number',None)
        branch_id = profile_credentials.get('branch')
        branch = Branch.query.filter_by(id=branch_id).first()
        cgpa = profile_credentials.get('cgpa',None)
        graduation_year = profile_credentials.get('graduation_year',None)
        phone = profile_credentials.get('phone',None)
        resume = profile_credentials.get('resume',None)

        if not (full_name and roll_number and cgpa and graduation_year and branch):
            result = {
                "message" : "Please fill the required fields"
            }
            return make_response(result,400)
        if len(full_name) < 3:
            result = {
                "message" : "Name too short"
            }
            return make_response(result,400)
        if cgpa<=0 and cgpa>=10:
            result = {
                "message" : "CGPA must be within 0 to 10"
            }
            return make_response(result,400)
        if graduation_year<1950 and graduation_year>2069:
            result = {
                "message" : "Please fill a valid graduation year"
            }
            return make_response(result,400)
        if phone:
            if not phone.isdigit() and len(phone)<10:
                result = {
                    "message" : "Please fill a valid phone number"
                }
                return make_response(result,400)
        
        info = Student(
            user_id = user_id,
            full_name=full_name,
            roll_number=roll_number,
            branch=branch,
            cgpa=cgpa,
            graduation_year=graduation_year,
            phone=phone,
            resume=resume
        )

        db.session.add(info)
        db.session.commit()

        return make_response({"message":"Your profile is now completed"},201)

    @jwt_required
    def put(self):
        pass

