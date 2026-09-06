from datetime import datetime

from database import db


class ClarificationStatus:
    OPEN = 'Open'
    ANSWERED = 'Answered'
    CLOSED = 'Closed'


class ClarificationRequest(db.Model):
    __tablename__ = 'clarification_requests'
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey('tasks.id'), nullable=False)
    raised_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    assigned_to = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    question = db.Column(db.Text, nullable=False)
    answer = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(32), default=ClarificationStatus.OPEN)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    resolved_at = db.Column(db.DateTime, nullable=True)

    assigned_to_user = db.relationship('User', foreign_keys=[assigned_to], lazy='joined')

    def __repr__(self):
        return f'<ClarificationRequest {self.id} on task {self.task_id}>'