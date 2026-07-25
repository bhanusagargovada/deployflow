from models.user import User
from database import db


def record_activity(user, action, meta=None):
    from models.activity import ActivityLog
    a = ActivityLog(user_id=user.id if user else None, action=action, meta=meta)
    db.session.add(a)
    db.session.commit()
