from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import request
from controllers.database import db
from controllers.models import *

class AdminDashboard(Resource):
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()

        user = User.query.get(user_id)

        if user.role != "admin":
            return {"message":"Access denied"},403

        return {
            "students":Student.query.count(),
            "companies":Company.query.count(),
            "drives":Drive.query.count(),
            "applications":Application.query.count(),
            "pending_companies":Company.query.filter_by(approval_status="pending").count(),
            "approved_companies":Company.query.filter_by(approval_status="approved").count(),
            "rejected_companies":Company.query.filter_by(approval_status="rejected").count(),
            "pending_drives":Drive.query.filter_by(approval_status="pending").count(),
            "approved_drives":Drive.query.filter_by(approval_status="approved").count(),
            "rejected_drives":Drive.query.filter_by(approval_status="rejected").count()
        },200
    
class AdminCompanies(Resource):
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()

        user = User.query.get(user_id)

        if user.role != "admin":
            return {"message":"Access denied"},403

        companies = Company.query.all()

        result = []

        for company in companies:
            result.append({
                "id":company.id,
                "company_name":company.company_name,
                "website":company.website,
                "hr_name":company.hr_name,
                "hr_email":company.hr_email,
                "approval_status":company.approval_status
            })

        return result,200
    
class AdminCompany(Resource):
    @jwt_required()
    def put(self, company_id):
        user_id = get_jwt_identity()

        user = User.query.get(user_id)

        if user.role != "admin":
            return {"message":"Access denied"},403

        company = Company.query.get(company_id)

        if not company:
            return {"message":"Company not found"},404

        company_credentials = request.get_json()

        if not company_credentials:
            return {"message":"Data are required"},400

        approval_status = company_credentials.get("approval_status",None)

        if approval_status not in ["approved","rejected"]:
            return {"message":"Invalid approval status"},400

        company.approval_status = approval_status

        db.session.commit()

        return {
            "message":"Company updated successfully"
        },200
    
class AdminDrives(Resource):
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()

        user = User.query.get(user_id)

        if user.role != "admin":
            return {"message":"Access denied"},403

        drives = Drive.query.all()

        result = []

        for drive in drives:
            result.append({
                "id":drive.id,
                "company":drive.company.company_name,
                "title":drive.title,
                "salary_package":drive.salary_package,
                "location":drive.location,
                "application_deadline":drive.application_deadline,
                "drive_date":drive.drive_date,
                "approval_status":drive.approval_status,
                "status":drive.status
            })

        return result,200