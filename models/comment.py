from datetime import datetime, timezone

from database import db


class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey('tasks.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    parent_id = db.Column(db.Integer, db.ForeignKey('comments.id'), nullable=True)
    content = db.Column(db.Text, nullable=False)
    attachment_path = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    user = db.relationship('User', lazy='joined')
    replies = db.relationship('Comment', backref=db.backref('parent', remote_side=[id]), lazy='dynamic')
    read_receipts = db.relationship('CommentReadReceipt', backref='comment', cascade='all, delete-orphan', lazy='dynamic')

    @property
    def message(self):
        return self.content

    @message.setter
    def message(self, value):
        self.content = value

    def seen_by(self, user_id):
        return self.read_receipts.filter_by(user_id=user_id).first() is not None

    def get_replies(self):
        return self.replies.order_by(Comment.created_at.asc()).all()

    def __repr__(self):
        return f'<Comment {self.id} on task {self.task_id}>'


class CommentReadReceipt(db.Model):
    __tablename__ = 'comment_read_receipts'
    id = db.Column(db.Integer, primary_key=True)
    comment_id = db.Column(db.Integer, db.ForeignKey('comments.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    seen_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    user = db.relationship('User', lazy='joined')

    __table_args__ = (
        db.UniqueConstraint('comment_id', 'user_id', name='uq_comment_read_receipt'),
    )
