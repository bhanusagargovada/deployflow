from database import db
from models.notification import Notification
from utils.email_utils import send_email
from models.user import User


def create_notification(user_id, message, link=None):
    n = Notification(user_id=user_id, message=message, link=link)
    db.session.add(n)
    db.session.commit()
    # send email if user has email configured
    user = User.query.get(user_id)
    if user and user.email:
        send_email('Notification - Project Tracker', [user.email], f'{message}\n\nOpen: {link or ""}')
    return n


def send_digest(user_id):
    user = User.query.get(user_id)
    if not user or not user.email:
        return None
    notes = Notification.query.filter_by(user_id=user_id, is_read=False).order_by(Notification.created_at.asc()).all()
    if not notes:
        send_email('Notification Digest - Project Tracker', [user.email], 'You have no new notifications.')
        return []
    body_lines = ['Your unread notifications:']
    for n in notes:
        body_lines.append(f'- {n.message} (at {n.created_at}) -> {n.link or ""}')
    body = '\n'.join(body_lines)
    send_email('Notification Digest - Project Tracker', [user.email], body)
    return notes
