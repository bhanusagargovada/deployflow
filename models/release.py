from database import db
from datetime import datetime


class ReleaseStatus:
    SUCCESS = 'Success'
    FAILED = 'Failed'
    ROLLBACK = 'Rollback'


class Release(db.Model):
    __tablename__ = 'releases'
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'))
    version = db.Column(db.String(64), nullable=False)
    release_date = db.Column(db.Date)
    notes = db.Column(db.Text)
    status = db.Column(db.String(32), default=ReleaseStatus.SUCCESS)
    released_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Release {self.version}>'
