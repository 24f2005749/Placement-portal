from flask import Flask
from flask_restful import Api, Resource
from controllers.config import Config
from controllers.database import db
from controllers.models import *
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from controllers.auth import Login, Register
from controllers.routes.students import StudentProfile
from controllers.routes.company import CompanyProfile
from controllers.routes.drives import DrivesList, CompanyDrive
from controllers.routes.applications import CompanyApplication, CompanyApplicationList, StudentApplication, StudentApplicationList
from controllers.routes.admin import AdminCompanies, AdminCompany, AdminDashboard, AdminDrive, AdminDrives, AdminApplications, AdminSearch, AdminStudents, AdminStudent
from controllers.routes.branches import BranchList, BranchResource
from controllers.routes.student_dashboard import StudentDashboard
from controllers.routes.company_dashboard import CompanyDashboard
from controllers.routes.student_drives import StudentDrives,StudentDrive,StudentCompanies
from controllers.routes.jobs import JobStatus, StudentApplicationExport, StudentApplicationExportFile

jwt = JWTManager()


def create_app():
    app = Flask(__name__)
    CORS(app,resources={r"/*": {"origins": ["http://localhost:5173","http://127.0.0.1:5173"]}})
    app.config.from_object(Config)
   

    db.init_app(app)
    jwt.init_app(app)
    api = Api(app)

    @jwt.expired_token_loader
    def token_expiration_message(jwt_header, jwt_payload):
        return {
            "message" : "Session expired. Please login again"
        }, 401

    with app.app_context():
        db.create_all()
        admin = User.query.filter_by(email="admin@gmail.com").first()

        if admin is None:
            admin = User(
                email="admin@gmail.com",
                role="admin",
                active=True
        )
            admin.set_password("admin123")
            
            db.session.add(admin)
            db.session.commit()

        def seed_branches():  
            branches = [
                "B.Tech CSE",
                "B.Tech IT",
                "B.Tech ECE",
                "B.Tech ME",
                "B.Tech CE"
            ]

            for branch_name in branches:
                if not Branch.query.filter_by(name=branch_name).first():
                    db.session.add(Branch(name=branch_name))

            db.session.commit()

        seed_branches()    

        Drive.query.filter(Drive.status.is_(None)).update({"status":"open"})
        Drive.query.filter(Drive.approval_status.is_(None)).update({"approval_status":"pending"})
        db.session.commit()
    return app,api

app, api = create_app()

#Routes

api.add_resource(Login,"/login")
api.add_resource(Register, "/register")

api.add_resource(StudentProfile,"/student/profile")
api.add_resource(CompanyProfile,"/company/profile")

api.add_resource(CompanyDrive,"/company/drives/<int:drive_id>")
api.add_resource(DrivesList,"/company/drives")

api.add_resource(StudentApplicationList,"/student/applications")

api.add_resource(StudentApplication,"/student/applications/<int:application_id>")

api.add_resource(CompanyApplicationList,"/company/drives/<int:drive_id>/applications")

api.add_resource(CompanyApplication,"/company/applications/<int:application_id>")

api.add_resource(AdminDashboard,"/admin/dashboard")

api.add_resource(AdminCompanies,"/admin/companies")
api.add_resource(AdminCompany,"/admin/companies/<int:company_id>")

api.add_resource(AdminDrives,"/admin/drives")
api.add_resource(AdminDrive,"/admin/drives/<int:drive_id>")

api.add_resource(AdminApplications,"/admin/applications")
api.add_resource(AdminSearch,"/admin/search")
api.add_resource(AdminStudents,"/admin/students")
api.add_resource(AdminStudent,"/admin/students/<int:student_id>")

api.add_resource(BranchList,"/branches")
api.add_resource(BranchResource,"/branches/<int:branch_id>")

api.add_resource(StudentDashboard,"/student/dashboard")

api.add_resource(CompanyDashboard,"/company/dashboard")

api.add_resource(StudentDrives,"/student/drives")
api.add_resource(StudentDrive,"/student/drives/<int:drive_id>")
api.add_resource(StudentCompanies,"/student/companies")
api.add_resource(StudentApplicationExport,"/student/applications/export")
api.add_resource(StudentApplicationExportFile,"/student/applications/export/<string:filename>")
api.add_resource(JobStatus,"/jobs/<string:job_id>")

if __name__=="__main__":
    app.run(port=3000,debug=True)
