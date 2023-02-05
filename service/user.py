import base64
import hashlib
import hmac

from helpers.constans import PWD_HASH_SALT, PWD_HASH_ITERATIONS
from dao.user import UserDAO


class UserService:
    def __init__(self, dao: UserDAO):
        self.dao = dao

    def get_one(self, uid):
        return self.dao.get_user_by_id(uid)

    def get_all(self):
        users = self.dao.get_all()
        return users

    def get_by_username(self, username):
        return self.dao.get_user_by_username(username)

    def get_hash(self, password):
        hash_digest = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),  # Convert the password to bytes
            PWD_HASH_SALT,
            PWD_HASH_ITERATIONS
        )

        return hmac.compare_digest(hash_digest)

    def compare_password(self, password, hash):
        decode_digest = base64.b64decode(hash)

        hash_digest = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),  # Convert the password to bytes
            PWD_HASH_SALT,
            PWD_HASH_ITERATIONS
        )

        return hmac.compare_digest(decode_digest, hash_digest)

    def create(self, user_d):
        user_d['password'] == self.get_hash(user_d['password'])

        return self.dao.create(user_d)

    def update(self, user_d):
        user_d['password'] == self.get_hash(user_d['password'])

        return self.dao.update(user_d)

