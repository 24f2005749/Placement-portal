from flask import Flask
from flask_restful import Api, Resource
from controllers.config import Config
from controllers.database import db
from controllers.models import *
from flask_jwt_extended import JWTManager, jwt_required
from controllers.auth import Login, Register
from controllers.routes.students import StudentProfile
from controllers.routes.company import CompanyProfile
from controllers.routes.drives import DrivesList, CompanyDrives
from controllers.routes.applications import CompanyApplication, CompanyApplicationList, StudentApplication, StudentApplicationList

jwt = JWTManager()

def create_app():
    app = Flask(__name__)
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

        #! TEMPORARY ADDITION 
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
        #! UPTO HERE
    return app,api

app, api = create_app()

#Routes

class Hello(Resource):
    def get(self):
        return "its working", 200
    def post(self):
        return "post also worked and created something", 201


class Protected(Resource):
    @jwt_required()
    def get(self):
        return "you are protected", 200

api.add_resource(Hello,"/")
api.add_resource(Protected,"/protected")



api.add_resource(Login,"/login")
api.add_resource(Register, "/register")

api.add_resource(StudentProfile,"/student/profile")
api.add_resource(CompanyProfile,"/company/profile")

api.add_resource(CompanyDrives)
api.add_resource(DrivesList,"/company/driveslist")

api.add_resource(StudentApplicationList,"/student/applications")

api.add_resource(StudentApplication,"/student/applications/<int:application_id>")

api.add_resource(CompanyApplicationList,"/company/drives/<int:drive_id>/applications")

api.add_resource(CompanyApplication,"/company/applications/<int:application_id>")

if __name__=="__main__":
    app.run(port=3000,debug=True)
