from flask import request
from flask_restx import Namespace, Resource

from dao.model.user import User, UserSchema
from implemented import user_service

user_ns = Namespace('users')
auth_ns = Namespace('auth')


@user_ns.route('/')
class UserView(Resource):
    def get(self):
        all_users = user_service.get_all()
        res = UserSchema(many=True).dump(all_users)
        return res, 200

    def post(self):
        req_json = request.json
        new_user = user_service.create(req_json)
        return "", 201, {"location": f"/users/{new_user.id}"}


@user_ns.route('/<int:uid>')
class UserView(Resource):
    def get(self, uid):
        user = user_service.get_one(uid)
        res = UserSchema().dump(user)
        return res, 200

    def put(self, uid):
        req_json = request.json
        if "id" not in req_json:
            req_json["id"] = uid
        user_service.update(req_json)
        return "", 204

    def delete(self, uid):
        user_service.delete(uid)
        return "", 204
