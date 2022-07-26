from . import db, login_manager, bcrypt
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(32))
    phone = db.Column(db.String(32))
    short_info = db.Column(db.String(32))
    experience = db.Column(db.Integer())
    preferred_position = db.Column(db.String(32))
    user = db.relationship('User', backref=db.backref('employees'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32))
    password_hash = db.Column(db.String(44))

    @property
    def password(self):
        return self.password_hash

    @password.setter
    def password(self, password_to_hash):
        self.password_hash = bcrypt.generate_password_hash(password_to_hash).decode('utf-8')

    def check_password(self, password_to_check):
        return bcrypt.check_password_hash(self.password_hash, password_to_check)