from database import db
from datetime import datetime, timezone


class TaskStatus:
    TODO = 'To Do'
    IN_PROGRESS = 'In Progress'
    DONE = 'Done'
    BLOCKED = 'Blocked'


class Task(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    priority = db.Column(db.String(20), default='Medium')
    deadline = db.Column(db.Date)
    status = db.Column(db.String(32), default=TaskStatus.TODO)
    progress = db.Column(db.Integer, default=0)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'))
    assigned_to = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    assignee = db.relationship('User', foreign_keys=[assigned_to], lazy='joined')
    comments = db.relationship('Comment', backref='task', cascade='all, delete-orphan', lazy='dynamic')
    clarification_requests = db.relationship('ClarificationRequest', backref='task', cascade='all, delete-orphan', lazy='dynamic')

    def __repr__(self):
        return f'<Task {self.title}>'
