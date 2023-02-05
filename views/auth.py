from flask import request
from flask_restx import Namespace, Resource

from implemented import auth_service

auth_ns = Namespace('auth')


@auth_ns.route('/')
class AuthViews(Resource):

    def post(self):
        req_js = request.json

        username = req_js.get('username')
        password = req_js.get('password')

        if None is [username, password]:
            return 404

        tokens = auth_service.generate_token(username, password)

        return tokens, 201

    def put(self):
        req_js = request.json
        token = req_js.get('refresh_token')

        if token is None:
            return 404

        tokens = auth_service.refresh_token(token)

        return tokens, 201
