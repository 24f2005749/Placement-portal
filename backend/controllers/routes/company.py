from controllers.database import db
from controllers.models import *
from flask_restful import Resource
from flask import request, jsonify, make_response
from flask_jwt_extended import jwt_required, get_jwt_identity

class CompanyProfile(Resource):
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()

        user = User.query.get(user_id)

        if user.role != "company":
            return {"message":"Access denied"},403

        company = Company.query.filter_by(user_id=user_id).first()

        if not company:
            return {"message":"Company profile not found"},404

        return {
            "company_name": company.company_name,
            "website": company.website,
            "hr_name": company.hr_name,
            "hr_email": company.hr_email,
            "description": company.description,
            "approval_status": company.approval_status,
            
        },200
    
    @jwt_required()
    def post(self):
        user_id = get_jwt_identity()

        user = User.query.get(user_id)

        if user.role != "company":
            return {"message": "Access denied"}, 403

        profile_credentials = request.get_json()

        # data validation
        if not profile_credentials:
            result = {
                "message":"Data are requied"
            }
            return make_response(result,400)
        
        company_name = profile_credentials.get('company_name',None)
        website = profile_credentials.get('website',None)
        hr_name = profile_credentials.get('hr_name')
        hr_email = profile_credentials.get('hr_email',None)
        description = profile_credentials.get('description',None)

        if not (company_name):
            result = {
                "message" : "Please fill the required fields"
            }
            return make_response(result,400)
        
        info = Company(
            user_id=user_id,
            company_name=company_name,
            website=website,
            hr_name=hr_name,
            hr_email=hr_email,
            description=description
        )

        user.profile_completed = True

        db.session.add(info)
        db.session.commit()

        return make_response({"message":"Your profile is now completed"},201)

    @jwt_required()
    def put(self):
        user_id = get_jwt_identity()

        user = User.query.get(user_id)

        if user.role != "company":
            return {"message":"Access denied"},403

        company = Company.query.filter_by(user_id=user_id).first()

        if not company:
            return {"message":"Company profile not found"},404

        profile_credentials = request.get_json()

        if not profile_credentials:
            return {"message":"Data are required"},400

        company_name = profile_credentials.get('company_name',company.company_name)
        website = profile_credentials.get('website',company.website)
        hr_name = profile_credentials.get('hr_name',company.hr_name)
        hr_email = profile_credentials.get('hr_email',company.hr_email)
        description = profile_credentials.get('description',company.description)

        if not company_name:
            return {"message":"Please fill the required fields"},400

        company.company_name = company_name
        company.website = website
        company.hr_name = hr_name
        company.hr_email = hr_email
        company.description = description

        db.session.commit()

        return {"message":"Profile updated successfully"},200
