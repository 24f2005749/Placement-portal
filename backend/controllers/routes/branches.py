from flask_restful import Resource
from controllers.models import *
from controllers.models import Branch as BranchModel
from controllers.database import db
from controllers.cache import cache_get, cache_set, clear_api_cache
from flask import request
from flask_jwt_extended import jwt_required,get_jwt_identity

def is_admin():
    user=User.query.get(get_jwt_identity())
    return user and user.role=="admin"

class BranchList(Resource):
    def get(self):
        cached = cache_get("api:branches")

        if cached:
            return cached,200

        branches = BranchModel.query.all()
        result = []
        for branch in branches:
            result.append({"id":branch.id,"name":branch.name})

        cache_set("api:branches", result, 900)

        return result,200

    @jwt_required()
    def post(self):
        if not is_admin():
            return {"message":"Access denied"},403

        branch_credentials=request.get_json()

        if not branch_credentials:
            return {"message":"Data are required"},400

        name=branch_credentials.get("name",None)

        if not name:
            return {"message":"Branch name is required"},400

        if BranchModel.query.filter_by(name=name).first():
            return {"message":"Branch already exists"},409

        branch=BranchModel(name=name)
        db.session.add(branch)
        db.session.commit()
        clear_api_cache()

        return {"message":"Branch created successfully","id":branch.id},201

class BranchResource(Resource):
    @jwt_required()
    def put(self,branch_id):
        if not is_admin():
            return {"message":"Access denied"},403

        branch=BranchModel.query.get(branch_id)

        if not branch:
            return {"message":"Branch not found"},404

        branch_credentials=request.get_json()

        if not branch_credentials:
            return {"message":"Data are required"},400

        name=branch_credentials.get("name",None)

        if not name:
            return {"message":"Branch name is required"},400

        existing=BranchModel.query.filter_by(name=name).first()

        if existing and existing.id!=branch.id:
            return {"message":"Branch already exists"},409

        branch.name=name
        db.session.commit()
        clear_api_cache()

        return {"message":"Branch updated successfully"},200

    @jwt_required()
    def delete(self,branch_id):
        if not is_admin():
            return {"message":"Access denied"},403

        branch=BranchModel.query.get(branch_id)

        if not branch:
            return {"message":"Branch not found"},404

        if branch.students or branch.drives:
            return {"message":"Branch is already in use"},400

        db.session.delete(branch)
        db.session.commit()
        clear_api_cache()

        return {"message":"Branch deleted successfully"},200
