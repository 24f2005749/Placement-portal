from flask import Flask
from flask_restful import Api, Resource
from controllers.config import Config
from controllers.database import db
from controllers.models import *
from flask_jwt_extended import JWTManager, jwt_required

jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    jwt.init_app(app)
    api = Api(app)

    with app.app_context():
        db.create_all()
        admin = User.query.filter_by(username="admin").first()

        if admin is None:
            admin = User(
                username="admin",
                email="admin@gmail.com",
                password=generate_password_hash("admin123"),
                role="admin",
                active=True
        )
            
            db.session.add(admin)
            db.session.commit()

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

from controllers.auth import Login

api.add_resource(Login,"/login")

if __name__=="__main__":
    app.run(port=3000,debug=True)
