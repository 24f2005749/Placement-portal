from flask_restful import Resource
from flask_jwt_extended import jwt_required,get_jwt_identity

from controllers.cache import cache_get, cache_set
from controllers.models import *

class StudentDashboard(Resource):

    @jwt_required()
    def get(self):

        user_id = get_jwt_identity()
        cache_key = f"api:student-dashboard:{user_id}"
        cached = cache_get(cache_key)

        if cached:
            return cached,200

        user=User.query.get(user_id)

        if user.role!="student":

            return {"message":"Access denied"},403

        student=user.student

        if not student:

            return {"message":"Student profile not found"},404

        applications=Application.query.filter_by(
            student_id=student.id
        ).all()

        selected=0
        pending=0

        for application in applications:

            if application.status=="selected":

                selected+=1

            elif application.status=="applied":

                pending+=1

        drives=Drive.query.filter_by(
            approval_status="approved",
            status="open"
        ).all()

        payload = {

            "eligible_drives":len(drives),

            "applications":len(applications),

            "selected":selected,

            "pending":pending

        }

        cache_set(cache_key, payload, 180)

        return payload,200
