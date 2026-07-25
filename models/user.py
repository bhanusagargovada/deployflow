from database import db, bcrypt, login_manager
from flask_login import UserMixin
from datetime import datetime


class Role:
    ADMIN = 'Administrator'
    PM = 'Project Manager'
    MEMBER = 'Team Member'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(32), default=Role.MEMBER)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)

    projects = db.relationship('Project', backref='owner', lazy=True)
    activities = db.relationship('ActivityLog', backref='user', lazy=True)

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    def is_admin(self):
        return self.role == Role.ADMIN

    def __repr__(self):
        return f'<User {self.username}>'
