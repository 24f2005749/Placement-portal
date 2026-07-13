from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import request
from controllers.cache import cache_get, cache_set, clear_api_cache
from controllers.database import db
from controllers.models import *

def serialize_company(company):
    return {
        "id":company.id,
        "user_id":company.user_id,
        "email":company.user.email,
        "company_name":company.company_name,
        "website":company.website,
        "hr_name":company.hr_name,
        "hr_email":company.hr_email,
        "description":company.description,
        "approval_status":company.approval_status,
        "active":company.user.active
    }

def serialize_student(student):
    return {
        "id":student.id,
        "user_id":student.user_id,
        "email":student.user.email,
        "full_name":student.full_name,
        "roll_number":student.roll_number,
        "branch":student.branch.name,
        "branch_id":student.branch_id,
        "cgpa":student.cgpa,
        "graduation_year":student.graduation_year,
        "phone":student.phone,
        "resume":student.resume,
        "active":student.user.active
    }

def serialize_drive(drive):
    return {
        "id":drive.id,
        "company":drive.company.company_name,
        "company_name":drive.company.company_name,
        "title":drive.title,
        "job_description":drive.job_description,
        "salary_package":drive.salary_package,
        "location":drive.location,
        "eligibility_year":drive.eligibility_year,
        "eligibility_cgpa":drive.eligibility_cgpa,
        "application_deadline":drive.application_deadline.isoformat() if drive.application_deadline else None,
        "drive_date":drive.drive_date.isoformat() if drive.drive_date else None,
        "approval_status":drive.approval_status,
        "status":drive.status,
        "eligible_branches":[branch.id for branch in drive.branches],
        "applications_count":len(drive.applications)
    }

def format_datetime(value):
    return value.isoformat() if value else None

class AdminDashboard(Resource):
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        cached = cache_get("api:admin-dashboard")

        user = User.query.get(user_id)

        if user.role != "admin":
            return {"message":"Access denied"},403

        if cached:
            return cached,200

        payload = {
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
        }

        cache_set("api:admin-dashboard", payload, 180)

        return payload,200
    
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
            result.append(serialize_company(company))

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

        approval_status = company_credentials.get("approval_status",company.approval_status)
        active = company_credentials.get("active",company.user.active)

        if approval_status not in ["pending","approved","rejected"]:
            return {"message":"Invalid approval status"},400

        company.approval_status = approval_status
        company.user.active = active

        db.session.commit()
        clear_api_cache()

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
            result.append(serialize_drive(drive))

        return result,200

class AdminDrive(Resource):
    @jwt_required()
    def get(self, drive_id):
        user_id = get_jwt_identity()

        user = User.query.get(user_id)

        if user.role != "admin":
            return {"message":"Access denied"},403

        drive = Drive.query.get(drive_id)

        if not drive:
            return {"message":"Drive not found"},404

        return serialize_drive(drive),200

    @jwt_required()
    def put(self, drive_id):
        user_id = get_jwt_identity()

        user = User.query.get(user_id)

        if user.role != "admin":
            return {"message":"Access denied"},403

        drive = Drive.query.get(drive_id)

        if not drive:
            return {"message":"Drive not found"},404

        drive_credentials = request.get_json()

        if not drive_credentials:
            return {"message":"Data are required"},400

        approval_status = drive_credentials.get("approval_status",drive.approval_status)
        status = drive_credentials.get("status",drive.status or "open")

        if approval_status not in ["pending","approved","rejected"]:
            return {"message":"Invalid approval status"},400

        if status not in ["open","closed"]:
            return {"message":"Invalid status"},400

        drive.approval_status = approval_status
        drive.status = status

        db.session.commit()
        clear_api_cache()

        return {
            "message":"Drive updated successfully"
        },200

class AdminApplications(Resource):

    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()

        user = User.query.get(user_id)

        if user.role != 'admin':
            return {"message":"access denied"}, 403
        
        applications = Application.query.all()

        result = []

        for application in applications:
            result.append({
                "application_id":application.id,
                "student_name":application.student.full_name,
                "roll_number":application.student.roll_number,
                "branch": application.student.branch.name,
                "cgpa": application.student.cgpa,
                "company_name":application.drive.company.company_name,
                "drive_title":application.drive.title,
                "status":application.status,
                "applied_at":format_datetime(application.applied_at),
                "interview_date":format_datetime(application.interview_date),
                "remarks":application.remarks
            })

        return result,200

class AdminSearch(Resource):
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()

        user = User.query.get(user_id)

        if user.role != "admin":
            return {"message":"Access denied"},403

        query = request.args.get("q",None)

        if not query:
            return {"message":"Search query is required"},400

        students = Student.query.filter(
            Student.full_name.ilike(f"%{query}%")
        ).all()

        companies = Company.query.filter(
            Company.company_name.ilike(f"%{query}%")
        ).all()

        drives = Drive.query.filter(
            Drive.title.ilike(f"%{query}%")
        ).all()

        result = {
            "students":[],
            "companies":[],
            "drives":[]
        }

        for student in students:
            result["students"].append(serialize_student(student))

        for company in companies:
            result["companies"].append(serialize_company(company))

        for drive in drives:
            result["drives"].append(serialize_drive(drive))

        return result,200

class AdminStudents(Resource):
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()

        user = User.query.get(user_id)

        if user.role != "admin":
            return {"message":"Access denied"},403

        drive_id = request.args.get("drive_id", type=int)
        eligible = request.args.get("eligible")
        drive = Drive.query.get(drive_id) if drive_id else None

        if drive_id and not drive:
            return {"message":"Drive not found"},404

        students = Student.query.all()

        result = []

        for student in students:
            item = serialize_student(student)

            if drive:
                reasons = []

                if drive.eligibility_cgpa and student.cgpa < drive.eligibility_cgpa:
                    reasons.append("CGPA criteria not satisfied")

                if drive.eligibility_year and student.graduation_year != drive.eligibility_year:
                    reasons.append("Graduation year not eligible")

                if drive.branches and student.branch not in drive.branches:
                    reasons.append("Branch not eligible")

                item["eligible_for_drive"] = len(reasons) == 0
                item["eligibility_message"] = ", ".join(reasons)

                if eligible in ["true","false"]:
                    requested = eligible == "true"

                    if item["eligible_for_drive"] != requested:
                        continue

            result.append(item)

        return result,200

class AdminStudent(Resource):
    @jwt_required()
    def put(self,student_id):
        user_id = get_jwt_identity()

        user = User.query.get(user_id)

        if user.role != "admin":
            return {"message":"Access denied"},403

        student = Student.query.get(student_id)

        if not student:
            return {"message":"Student not found"},404

        student_credentials = request.get_json()

        if not student_credentials:
            return {"message":"Data are required"},400

        active = student_credentials.get("active",student.user.active)

        student.user.active = active
        db.session.commit()
        clear_api_cache()

        return {"message":"Student updated successfully"},200
