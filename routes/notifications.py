from flask import Blueprint, render_template, jsonify, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models.notification import Notification
from database import db

notifications_bp = Blueprint('notifications', __name__, url_prefix='/notifications', template_folder='../templates')


@notifications_bp.route('/')
@login_required
def list_notifications():
    notes = Notification.query.filter_by(user_id=current_user.id).order_by(Notification.created_at.desc()).all()
    return render_template('notifications/list.html', notifications=notes)


@notifications_bp.route('/api/unread_count')
@login_required
def unread_count():
    count = Notification.query.filter_by(user_id=current_user.id, is_read=False).count()
    return jsonify({'unread': count})


@notifications_bp.route('/<int:notif_id>/mark_read', methods=['POST'])
@login_required
def mark_read(notif_id):
    n = Notification.query.get_or_404(notif_id)
    if n.user_id != current_user.id:
        return ('', 403)
    n.is_read = True
    db.session.commit()
    return ('', 204)


@notifications_bp.route('/mark_all_read', methods=['POST'])
@login_required
def mark_all_read():
    Notification.query.filter_by(user_id=current_user.id, is_read=False).update({'is_read': True})
    db.session.commit()
    flash('All notifications marked read', 'success')
    return redirect(url_for('notifications.list_notifications'))


@notifications_bp.route('/send_digest', methods=['POST'])
@login_required
def send_digest():
    # send an email digest of unread notifications to the user
    from services.notification_service import send_digest
    send_digest(current_user.id)
    flash('Digest sent to your email (if configured).', 'info')
    return redirect(url_for('notifications.list_notifications'))
