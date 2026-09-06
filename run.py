from app import create_app
from database import db
import models

app = create_app()

if __name__ == '__main__':
    if app.config['SQLALCHEMY_DATABASE_URI'].startswith('sqlite'):
        with app.app_context():
            db.create_all()
    app.run(host='0.0.0.0', port=5000)
