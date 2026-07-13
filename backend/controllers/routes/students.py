from controllers.database import db
from controllers.models import *
from flask_restful import Resource
from flask import request, make_response
from flask_jwt_extended import jwt_required, get_jwt_identity
from urllib.parse import urlparse

def is_valid_resume_url(value):
    parsed = urlparse(value)
    return parsed.scheme in ["http", "https"] and bool(parsed.netloc)

def serialize_student(student):
    return {
        "id":student.id,
        "user_id":student.user_id,
        "email":student.user.email,
        "full_name":student.full_name,
        "roll_number":student.roll_number,
        "branch":student.branch_id,
        "branch_id":student.branch_id,
        "branch_name":student.branch.name,
        "cgpa":student.cgpa,
        "graduation_year":student.graduation_year,
        "phone":student.phone,
        "resume":student.resume,
        "active":student.user.active
    }

class StudentProfile(Resource):
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()

        student = Student.query.filter_by(user_id=user_id).first()

        if not student:
            return {"message": "Profile not found"}, 404

        return serialize_student(student), 200
    
    @jwt_required()
    def post(self):
        user_id = get_jwt_identity()

        user = User.query.get(user_id)

        if user.role != "student":
            return {"message": "Access denied"}, 403

        profile_credentials = request.get_json()

        if not profile_credentials:
            result = {
                "message":"Data are required"
            }
            return make_response(result,400)

        if Student.query.filter_by(user_id=user_id).first():
            return {"message":"Profile already exists"},409
        
        full_name = profile_credentials.get('full_name',None)
        roll_number = profile_credentials.get('roll_number',None)
        branch_id = profile_credentials.get('branch')
        branch = Branch.query.filter_by(id=branch_id).first()
        cgpa = profile_credentials.get('cgpa',None)
        graduation_year = profile_credentials.get('graduation_year',None)
        phone = profile_credentials.get('phone',None)
        resume = profile_credentials.get('resume') or None

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
        if cgpa<=0 or cgpa>=10:
            result = {
                "message" : "CGPA must be within 0 to 10"
            }
            return make_response(result,400)
        if graduation_year<1950 or graduation_year>2069:
            result = {
                "message" : "Please fill a valid graduation year"
            }
            return make_response(result,400)
        if phone:
            if not phone.isdigit() or len(phone)<10:
                result = {
                    "message" : "Please fill a valid phone number"
                }
                return make_response(result,400)

        if resume and not is_valid_resume_url(resume):
            return {"message":"Resume must be an absolute http(s) URL"},400
        
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
        user.profile_completed = True
        db.session.add(info)
        db.session.commit()

        

        return make_response({"message":"Your profile is now completed"},201)

    @jwt_required()
    def put(self):
        user_id = get_jwt_identity()

        user = User.query.get(user_id)

        if user.role != "student":
            return {"message":"Access denied"},403

        student = Student.query.filter_by(user_id=user_id).first()

        if not student:
            return {"message":"Student profile not found"},404

        profile_credentials = request.get_json()

        if not profile_credentials:
            return {"message":"Data are required"},400

        full_name = profile_credentials.get('full_name',student.full_name)
        roll_number = profile_credentials.get('roll_number',student.roll_number)
        branch_id = profile_credentials.get('branch',student.branch_id)
        branch = Branch.query.get(branch_id)
        cgpa = profile_credentials.get('cgpa',student.cgpa)
        graduation_year = profile_credentials.get('graduation_year',student.graduation_year)
        phone = profile_credentials.get('phone',student.phone)
        resume = profile_credentials.get('resume',student.resume) or None

        if len(full_name) < 3:
            return {"message":"Name too short"},400

        if cgpa < 0 or cgpa > 10:
            return {"message":"CGPA must be within 0 to 10"},400

        if graduation_year < 1950 or graduation_year > 2069:
            return {"message":"Please fill a valid graduation year"},400

        if not branch:
            return {"message":"Invalid branch"},400

        if phone and (not phone.isdigit() or len(phone) != 10):
            return {"message":"Please fill a valid phone number"},400

        if resume and not is_valid_resume_url(resume):
            return {"message":"Resume must be an absolute http(s) URL"},400

        student.full_name = full_name
        student.roll_number = roll_number
        student.branch = branch
        student.cgpa = cgpa
        student.graduation_year = graduation_year
        student.phone = phone
        student.resume = resume

        db.session.commit()

        return {"message":"Profile updated successfully"},200
