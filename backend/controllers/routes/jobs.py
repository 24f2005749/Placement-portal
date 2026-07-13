from celery.result import AsyncResult
from flask import send_from_directory
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Resource
from kombu.exceptions import OperationalError

from controllers.config import Config
from controllers.models import Student, User
from controllers.tasks import celery, export_student_applications


class StudentApplicationExport(Resource):
    @jwt_required()
    def post(self):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)

        if user.role != "student":
            return {"message":"Access denied"},403

        student = Student.query.filter_by(user_id=user_id).first()

        if not student:
            return {"message":"Student profile not found"},404

        try:
            job = export_student_applications.delay(student.id)
        except OperationalError:
            return {
                "message":"Redis is not running. Start Redis and the Celery worker before exporting."
            },503

        return {
            "message":"Export started. You will be alerted when it is ready.",
            "job_id":job.id
        },202


class JobStatus(Resource):
    @jwt_required()
    def get(self, job_id):
        job = AsyncResult(job_id, app=celery)

        response = {
            "job_id":job.id,
            "state":job.state
        }

        if job.successful():
            response["result"] = job.result
            response["message"] = "Export completed"
        elif job.failed():
            response["message"] = str(job.result)
        else:
            response["message"] = "Export is still running"

        return response,200


class StudentApplicationExportFile(Resource):
    @jwt_required()
    def get(self, filename):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)

        if user.role != "student":
            return {"message":"Access denied"},403

        student = Student.query.filter_by(user_id=user_id).first()

        if not student:
            return {"message":"Student profile not found"},404

        expected_prefix = f"student_{student.id}_applications_"

        if not filename.startswith(expected_prefix) or not filename.endswith(".csv"):
            return {"message":"File not found"},404

        return send_from_directory(Config.EXPORT_FOLDER, filename, as_attachment=True)
