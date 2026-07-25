from app import create_app
from config import DevelopmentConfig
from database import db
from models.user import User, Role


def seed(email='admin@example.com', username='admin', password='adminpass'):
    app = create_app(DevelopmentConfig)
    with app.app_context():
        db.create_all()
        if User.query.filter_by(email=email).first():
            print('Admin user already exists')
            return
        u = User(username=username, email=email, role=Role.ADMIN)
        u.set_password(password)
        db.session.add(u)
        db.session.commit()
        print('Created admin', email)


if __name__ == '__main__':
    seed()
