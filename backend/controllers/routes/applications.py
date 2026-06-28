from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import request
from datetime import date
from controllers.database import db
from controllers.models import *
from datetime import datetime


class StudentApplicationList(Resource):

    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()

        user = User.query.get(user_id)

        if user.role != "student":
            return {"message":"Access denied"},403

        student = Student.query.filter_by(user_id=user_id).first()

        if not student:
            return {"message":"Student profile not found"},404

        applications = Application.query.filter_by(student_id=student.id).all()

        result = []

        for application in applications:
            result.append({
                "application_id": application.id,
                "drive_id": application.drive.id,
                "company_name": application.drive.company.company_name,
                "title": application.drive.title,
                "status": application.status,
                "applied_at": application.applied_at
            })

        return result,200


    @jwt_required()
    def post(self):
        user_id = get_jwt_identity()

        user = User.query.get(user_id)

        if user.role != "student":
            return {"message":"Access denied"},403

        student = Student.query.filter_by(user_id=user_id).first()

        if not student:
            return {"message":"Student profile not found"},404

        application_credentials = request.get_json()

        if not application_credentials:
            return {"message":"Data are required"},400

        drive_id = application_credentials.get("drive_id",None)

        if not drive_id:
            return {"message":"Drive id is required"},400

        drive = Drive.query.get(drive_id)

        if not drive:
            return {"message":"Drive not found"},404

        if drive.approval_status != "approved":
            return {"message":"Drive not approved"},403

        if drive.status != "open":
            return {"message":"Drive is closed"},400

        if drive.application_deadline < date.today():
            return {"message":"Application deadline has passed"},400

        if drive.eligibility_cgpa and student.cgpa < drive.eligibility_cgpa:
            return {"message":"CGPA criteria not satisfied"},400

        if drive.eligibility_year and student.graduation_year != drive.eligibility_year:
            return {"message":"Graduation year not eligible"},400

        if student.branch not in drive.branches:
            return {"message":"Branch not eligible"},400

        existing_application = Application.query.filter_by(
            student_id=student.id,
            drive_id=drive.id
        ).first()

        if existing_application:
            return {"message":"Already applied"},409

        application = Application(
            student_id=student.id,
            drive_id=drive.id
        )

        db.session.add(application)
        db.session.commit()

        return {
            "message":"Application submitted successfully",
            "application_id":application.id
        },201
    
class StudentApplication(Resource):

    @jwt_required()
    def get(self, application_id):
        user_id = get_jwt_identity()

        user = User.query.get(user_id)

        if user.role != "student":
            return {"message":"Access denied"},403

        student = Student.query.filter_by(user_id=user_id).first()

        if not student:
            return {"message":"Student profile not found"},404

        application = Application.query.filter_by(
            id=application_id,
            student_id=student.id
        ).first()

        if not application:
            return {"message":"Application not found"},404

        return {
            "application_id":application.id,
            "company_name":application.drive.company.company_name,
            "title":application.drive.title,
            "job_description":application.drive.job_description,
            "salary_package":application.drive.salary_package,
            "location":application.drive.location,
            "status":application.status,
            "remarks":application.remarks,
            "interview_date":application.interview_date,
            "applied_at":application.applied_at
        },200

    @jwt_required()
    def delete(self, application_id):
        user_id = get_jwt_identity()

        user = User.query.get(user_id)

        if user.role != "student":
            return {"message":"Access denied"},403

        student = Student.query.filter_by(user_id=user_id).first()

        if not student:
            return {"message":"Student profile not found"},404

        application = Application.query.filter_by(
            id=application_id,
            student_id=student.id
        ).first()

        if not application:
            return {"message":"Application not found"},404

        if application.status != "applied":
            return {"message":"Application cannot be withdrawn"},400

        db.session.delete(application)
        db.session.commit()

        return {"message":"Application withdrawn successfully"},200
    

class CompanyApplication(Resource):

    @jwt_required()
    def put(self, application_id):
        user_id = get_jwt_identity()

        user = User.query.get(user_id)

        if user.role != "company":
            return {"message":"Access denied"},403

        company = Company.query.filter_by(user_id=user_id).first()

        if not company:
            return {"message":"Company profile not found"},404

        application = Application.query.get(application_id)

        if not application:
            return {"message":"Application not found"},404

        if application.drive.company_id != company.id:
            return {"message":"Access denied"},403

        application_credentials = request.get_json()

        if not application_credentials:
            return {"message":"Data are required"},400

        status = application_credentials.get("status",application.status)
        remarks = application_credentials.get("remarks",application.remarks)
        interview_date = application_credentials.get("interview_date",None)

        allowed_status = [
            "applied",
            "shortlisted",
            "selected",
            "rejected"
        ]

        if status not in allowed_status:
            return {"message":"Invalid status"},400

        application.status = status
        application.remarks = remarks

        if interview_date:
            try:
                application.interview_date = datetime.strptime(
                    interview_date,
                    "%Y-%m-%d %H:%M"
                )
            except ValueError:
                return {
                    "message":"Date must be YYYY-MM-DD HH:MM"
                },400

        db.session.commit()

        return {"message":"Application updated successfully"},200