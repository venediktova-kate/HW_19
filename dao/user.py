from dao.model.user import User


class UserDAO:
    def __init__(self, session):
        self.session = session

    def get_all(self):
        return self.session.query(User).all()

    def get_user_by_id(self, uid):
        return self.session.query(User).get(uid)

    def get_user_by_username(self, username):
        return self.session.query(User).filter(User.usernamem == username).first()

    def create(self, user_d):
        new = User(**user_d)

        self.session.add(new)
        self.session.commit()
        return new

    def delete(self, uid):
        user = self.get_user_by_id(uid)

        self.session.delete(user)
        self.session.commit()

    def update(self, user_d):
        user = self.get_user_by_id(user_d.get("id"))
        user.username = user_d.get("username")
        user.password = user_d.get("password")
        user.role = user_d.get("role")

        self.session.add(user)
        self.session.commit()
