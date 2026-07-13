from flask_restful import Resource
from flask_jwt_extended import jwt_required,get_jwt_identity

from controllers.models import *

class CompanyDashboard(Resource):

    @jwt_required()
    def get(self):

        user=User.query.get(get_jwt_identity())

        if user.role!="company":

            return {"message":"Access denied"},403

        company=user.company

        if not company:

            return {"message":"Company profile not found"},404

        drives=Drive.query.filter_by(
            company_id=company.id
        ).all()

        applicants=0
        pending=0

        for drive in drives:

            applicants+=len(drive.applications)

            if drive.approval_status=="pending":

                pending+=1

        return{

            "drives":len(drives),

            "applicants":applicants,

            "pending":pending

        },200
