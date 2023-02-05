import calendar
import datetime

import jwt
from flask_restx import abort

from helpers.constans import SECRET, ALGO
from service.user import UserService


class AuthService:

    def __init__(self, user_service: UserService):
        self.user_service = user_service

    def generate_token(self, username, password, is_refresh = False):
        user = self.user_service.get_by_username(username)

        if user is None:
            abort(400)
        if not is_refresh:
            if not self.user_service.compare_password(user.password, password):
                abort(400)

        data = {
            'username': username,
            'role': user.role
        }

        min30 = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        data['exp'] = calendar.timegm(min30.timetuple())
        access_token = jwt.encode(data, SECRET, algorithm=ALGO)

        day30 = datetime.datetime.utcnow() + datetime.timedelta(days=30)
        data['exp'] = calendar.timegm(day30.timetuple())
        refresh_token = jwt.encode(data, SECRET, algorithm=ALGO)

        return {
            'access_token': access_token,
            'refresh_token': refresh_token
        }

    def refresh_token(self, token):
        data = jwt.decode(jwt=token, key=SECRET, algorithm=ALGO)
        username = data.get('username')

        return self.generate_token(username, None, is_refresh=True)