from datetime import datetime, timezone

from database import db


class StatusReportStatus:
    PENDING = 'Pending'
    APPROVED = 'Approved'
    CHANGES_REQUESTED = 'ChangesRequested'
    REJECTED = 'Rejected'


class StatusReport(db.Model):
    __tablename__ = 'status_reports'
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey('tasks.id'), nullable=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)
    submitted_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    report_date = db.Column(db.Date, default=lambda: datetime.now(timezone.utc).date())
    work_done = db.Column(db.Text, nullable=False)
    blockers = db.Column(db.Text, nullable=True)
    hours_spent = db.Column(db.Float, nullable=True)
    next_steps = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(32), default=StatusReportStatus.PENDING)
    manager_feedback = db.Column(db.Text, nullable=True)
    reviewed_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    reviewed_at = db.Column(db.DateTime, nullable=True)

    task = db.relationship('Task', lazy='joined')

    def __repr__(self):
        return f'<StatusReport {self.id} project={self.project_id}>'