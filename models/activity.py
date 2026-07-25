from database import db
from datetime import datetime


class ActivityLog(db.Model):
    __tablename__ = 'activity_logs'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    action = db.Column(db.String(200))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    meta = db.Column(db.Text)

    def __repr__(self):
        return f'<Activity {self.action} by {self.user_id}>'
