from database import db
from datetime import datetime


class ProjectStatus:
    PLANNED = 'Planned'
    ACTIVE = 'Active'
    COMPLETED = 'Completed'
    ON_HOLD = 'On Hold'


class Project(db.Model):
    __tablename__ = 'projects'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(140), nullable=False)
    description = db.Column(db.Text)
    priority = db.Column(db.String(20), default='Medium')
    deadline = db.Column(db.Date)
    status = db.Column(db.String(32), default=ProjectStatus.PLANNED)
    manager_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    tasks = db.relationship('Task', backref='project', lazy=True)
    releases = db.relationship('Release', backref='project', lazy=True)
    members = db.relationship('ProjectMember', backref='project', lazy=True)
    status_reports = db.relationship('StatusReport', backref='project', cascade='all, delete-orphan', lazy='dynamic')
    announcements = db.relationship('Announcement', backref='project', cascade='all, delete-orphan', lazy='dynamic')

    def __repr__(self):
        return f'<Project {self.name}>'
