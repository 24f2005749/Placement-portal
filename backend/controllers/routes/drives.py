from flask import request
from controllers.database import db
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource
from controllers.models import *
from datetime import datetime


class CompanyDrive(Resource):
    @jwt_required()
    def get(self, drive_id):
        user_id = get_jwt_identity()

        user = User.query.get(user_id)

        if user.role != "company":
            return {"message":"Access denied"},403

        company = Company.query.filter_by(user_id=user_id).first()

        if not company:
            return {"message":"Company profile not found"},404

        drive = Drive.query.filter_by(id=drive_id, company_id=company.id).first()

        if not drive:
            return {"message":"Drive not found"},404

        return {
            "id": drive.id,
            "title": drive.title,
            "job_description": drive.job_description,
            "salary_package": drive.salary_package,
            "location": drive.location,
            "eligibility_year": drive.eligibility_year,
            "eligibility_cgpa": drive.eligibility_cgpa,
            "application_deadline": drive.application_deadline,
            "drive_date": drive.drive_date,
            "approval_status": drive.approval_status,
            "status": drive.status,
            "eligible_branches":[branch.id for branch in drive.branches]
        },200

    @jwt_required()
    def put(self, drive_id):
        user_id = get_jwt_identity()

        user = User.query.get(user_id)

        if user.role != "company":
            return {"message":"Access denied"},403

        company = Company.query.filter_by(user_id=user_id).first()

        if not company:
            return {"message":"Company profile not found"},404

        drive = Drive.query.filter_by(id=drive_id, company_id=company.id).first()

        if not drive:
            return {"message":"Drive not found"},404

        drive_credentials = request.get_json()

        if not drive_credentials:
            return {"message":"Data are required"},400

        drive.title = drive_credentials.get('title',drive.title)
        drive.job_description = drive_credentials.get('job_description',drive.job_description)
        drive.salary_package = drive_credentials.get('salary_package',drive.salary_package)
        drive.location = drive_credentials.get('location',drive.location)
        drive.eligibility_year = drive_credentials.get('eligibility_year',drive.eligibility_year)
        drive.eligibility_cgpa = drive_credentials.get('eligibility_cgpa',drive.eligibility_cgpa)

        if drive.eligibility_cgpa and (drive.eligibility_cgpa < 0 or drive.eligibility_cgpa > 10):
            return {"message":"Invalid CGPA"},400

        application_deadline = drive_credentials.get('application_deadline',None)
        drive_date = drive_credentials.get('drive_date',None)

        if application_deadline:
            try:
                drive.application_deadline = datetime.strptime(application_deadline,"%Y-%m-%d").date()
            except ValueError:
                return {"message":"Date must be in YYYY-MM-DD format"},400

        if drive_date:
            try:
                drive.drive_date = datetime.strptime(drive_date,"%Y-%m-%d").date()
            except ValueError:
                return {"message":"Date must be in YYYY-MM-DD format"},400

        if 'eligible_branches' in drive_credentials:
            drive.branches.clear()

            for branch_id in drive_credentials['eligible_branches']:
                branch = Branch.query.get(branch_id)

                if branch:
                    drive.branches.append(branch)

        db.session.commit()

        return {"message":"Drive updated successfully"},200

    @jwt_required()
    def delete(self, drive_id):
        user_id = get_jwt_identity()

        user = User.query.get(user_id)

        if user.role != "company":
            return {"message":"Access denied"},403

        company = Company.query.filter_by(user_id=user_id).first()

        if not company:
            return {"message":"Company profile not found"},404

        drive = Drive.query.filter_by(id=drive_id, company_id=company.id).first()

        if not drive:
            return {"message":"Drive not found"},404

        db.session.delete(drive)
        db.session.commit()

        return {"message":"Drive deleted successfully"},200


class DrivesList(Resource):
    @jwt_required()
    def get(self):
        drives = Drive.query.filter_by(approval_status="approved", status="open").all()

        result = []

        for drive in drives:
            result.append({
                "id": drive.id,
                "company": drive.company.company_name,
                "title": drive.title,
                "salary_package": drive.salary_package,
                "location": drive.location,
                "application_deadline": drive.application_deadline
            })

        return result,200

    @jwt_required()
    def post(self):
        user_id = get_jwt_identity()

        user = User.query.get(user_id)

        if user.role != "company":
            return {"message":"Access denied"},403

        company = Company.query.filter_by(user_id=user_id).first()

        if not company:
            return {"message":"Company profile not found"},404

        drive_credentials = request.get_json()

        if not drive_credentials:
            return {"message":"Data are required"},400

        title = drive_credentials.get('title',None)
        job_description = drive_credentials.get('job_description',None)
        salary_package = drive_credentials.get('salary_package',None)
        location = drive_credentials.get('location',None)
        eligibility_year = drive_credentials.get('eligibility_year',None)
        eligibility_cgpa = drive_credentials.get('eligibility_cgpa',None)
        application_deadline = drive_credentials.get('application_deadline',None)
        drive_date = drive_credentials.get('drive_date',None)
        eligible_branches = drive_credentials.get('eligible_branches',[])

        if not (title and job_description and application_deadline):
            return {"message":"Please fill the required fields"},400

        if eligibility_cgpa and (eligibility_cgpa < 0 or eligibility_cgpa > 10):
            return {"message":"Invalid CGPA"},400

        try:
            application_deadline = datetime.strptime(application_deadline,"%Y-%m-%d").date()

            if drive_date:
                drive_date = datetime.strptime(drive_date,"%Y-%m-%d").date()

        except ValueError:
            return {"message":"Date must be in YYYY-MM-DD format"},400

        drive = Drive(
            company_id=company.id,
            title=title,
            job_description=job_description,
            salary_package=salary_package,
            location=location,
            eligibility_year=eligibility_year,
            eligibility_cgpa=eligibility_cgpa,
            application_deadline=application_deadline,
            drive_date=drive_date
        )

        for branch_id in eligible_branches:
            branch = Branch.query.get(branch_id)

            if branch:
                drive.branches.append(branch)

        db.session.add(drive)
        db.session.commit()

        return {
            "message":"Drive created successfully",
            "drive_id":drive.id
        },201