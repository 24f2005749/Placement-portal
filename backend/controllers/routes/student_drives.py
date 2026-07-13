from flask_restful import Resource
from flask import request
from sqlalchemy import or_
from flask_jwt_extended import jwt_required,get_jwt_identity
from datetime import date

from controllers.cache import cache_get, cache_set
from controllers.models import *

def format_date(value):
    return value.isoformat() if value else None

def eligibility_message(student, drive):
    reasons = []

    if drive.eligibility_cgpa and student.cgpa < drive.eligibility_cgpa:
        reasons.append("CGPA criteria not satisfied")

    if drive.eligibility_year and student.graduation_year != drive.eligibility_year:
        reasons.append("Graduation year not eligible")

    if drive.branches and student.branch not in drive.branches:
        reasons.append("Branch not eligible")

    return ", ".join(reasons)

def deadline_passed(drive):
    return bool(drive.application_deadline and drive.application_deadline < date.today())

class StudentDrives(Resource):

    @jwt_required()
    def get(self):

        user_id = get_jwt_identity()
        query = request.args.get("q", "").strip()
        cache_key = f"api:student-drives:{user_id}"

        if not query:
            cached = cache_get(cache_key)

            if cached:
                return cached,200

        user=User.query.get(user_id)

        if user.role!="student":

            return {"message":"Access denied"},403

        student=user.student

        if not student:

            return {"message":"Student profile not found"},404

        drives_query=Drive.query.filter_by(
            approval_status="approved",
            status="open"
        )

        if query:
            search = f"%{query}%"
            drives_query = drives_query.join(Company).filter(
                or_(
                    Drive.title.ilike(search),
                    Drive.location.ilike(search),
                    Company.company_name.ilike(search)
                )
            )

        drives=drives_query.all()

        result=[]

        for drive in drives:

            message = eligibility_message(student, drive)
            expired = deadline_passed(drive)

            result.append({

                "id":drive.id,

                "company_name":drive.company.company_name,

                "title":drive.title,

                "job_description":drive.job_description,

                "salary_package":drive.salary_package,

                "location":drive.location,

                "eligibility_cgpa":drive.eligibility_cgpa,

                "eligibility_year":drive.eligibility_year,

                "application_deadline":format_date(drive.application_deadline),

                "drive_date":format_date(drive.drive_date),

                "status": drive.status,

                "eligible": message == "",

                "eligibility_message": message,

                "deadline_passed": expired,

                "can_apply": message == "" and not expired

            })

        if not query:
            cache_set(cache_key, result, 180)

        return result,200


class StudentCompanies(Resource):

    @jwt_required()
    def get(self):
        user = User.query.get(get_jwt_identity())

        if user.role != "student":
            return {"message":"Access denied"},403

        query = request.args.get("q", "").strip()
        companies_query = Company.query.filter_by(approval_status="approved")

        if query:
            search = f"%{query}%"
            companies_query = companies_query.filter(
                or_(
                    Company.company_name.ilike(search),
                    Company.website.ilike(search),
                    Company.description.ilike(search)
                )
            )

        return [{
            "id": company.id,
            "company_name": company.company_name,
            "website": company.website,
            "description": company.description
        } for company in companies_query.order_by(Company.company_name).all()], 200
    
class StudentDrive(Resource):

    @jwt_required()
    def get(self,drive_id):

        user=User.query.get(get_jwt_identity())

        if user.role!="student":

            return {"message":"Access denied"},403

        student=user.student

        if not student:

            return {"message":"Student profile not found"},404

        drive=Drive.query.get(drive_id)

        if not drive:

            return{

                "message":"Drive not found"

            },404

        if drive.approval_status!="approved" or drive.status!="open":

            return {"message":"Drive not available"},404

        if drive.eligibility_cgpa and student.cgpa<drive.eligibility_cgpa:

            return {"message":"CGPA criteria not satisfied"},403

        if drive.eligibility_year and student.graduation_year!=drive.eligibility_year:

            return {"message":"Graduation year not eligible"},403

        if drive.branches and student.branch not in drive.branches:

            return {"message":"Branch not eligible"},403

        message = eligibility_message(student, drive)
        expired = deadline_passed(drive)

        return{

            "id":drive.id,

            "company_name":drive.company.company_name,

            "title":drive.title,

            "job_description":drive.job_description,

            "salary_package":drive.salary_package,

            "location":drive.location,

            "eligibility_cgpa":drive.eligibility_cgpa,

            "eligibility_year":drive.eligibility_year,

            "application_deadline":format_date(drive.application_deadline),

            "drive_date":format_date(drive.drive_date),

            "status": drive.status,

            "eligible": message == "",

            "eligibility_message": message,

            "deadline_passed": expired,

            "can_apply": message == "" and not expired

        },200
