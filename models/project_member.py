from database import db


class ProjectMember(db.Model):
    __tablename__ = 'project_members'
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    role = db.Column(db.String(64), default='Member')

    user = db.relationship('User', foreign_keys=[user_id], lazy='joined')

    def __repr__(self):
        return f'<ProjectMember project={self.project_id} user={self.user_id}>'
