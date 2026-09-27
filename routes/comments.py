import os
import re
from uuid import uuid4

from flask import Blueprint, request, redirect, url_for, flash, render_template, current_app
from flask_login import login_required, current_user
from forms.comment_forms import CommentForm
from database import db
from models.comment import Comment, CommentReadReceipt
from models.task import Task
from models.user import User
from services.auth_service import record_activity
from services.notification_service import create_notification
from werkzeug.utils import secure_filename

comments_bp = Blueprint('comments', __name__, url_prefix='/comments', template_folder='../templates')


ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf', 'txt', 'doc', 'docx'}


def _allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def _save_attachment(file_storage):
    if not file_storage or not file_storage.filename:
        return None
    if not _allowed_file(file_storage.filename):
        return None

    upload_dir = os.path.join(current_app.static_folder, 'uploads', 'comments')
    os.makedirs(upload_dir, exist_ok=True)

    filename = secure_filename(file_storage.filename)
    stored_name = f'{uuid4().hex}_{filename}'
    file_path = os.path.join(upload_dir, stored_name)
    file_storage.save(file_path)
    return url_for('static', filename=f'uploads/comments/{stored_name}')


@comments_bp.route('/create', methods=['POST'])
@login_required
def create_comment():
    form = CommentForm()
    if form.validate_on_submit():
        task = db.session.get(Task, form.task_id.data)
        if not task:
            flash('Task not found', 'danger')
            return redirect(request.referrer or url_for('tasks.list_tasks'))

        attachment = request.files.get('attachment')
        attachment_path = _save_attachment(attachment)
        if attachment and attachment.filename and not attachment_path:
            flash('Unsupported file type. Allowed: png, jpg, jpeg, gif, pdf, txt, doc, docx', 'danger')
            return redirect(request.referrer or url_for('tasks.list_tasks'))

        c = Comment(
            task_id=task.id,
            user_id=current_user.id,
            parent_id=form.parent_id.data or None,
            content=form.content.data,
            attachment_path=attachment_path,
        )
        db.session.add(c)
        db.session.commit()
        record_activity(current_user, 'create_comment', meta=str({'comment_id': c.id, 'task_id': task.id}))

        mentioned_usernames = set(re.findall(r'@([A-Za-z0-9_.]+)', form.content.data or ''))
        if mentioned_usernames:
            mentioned_users = User.query.filter(User.username.in_(mentioned_usernames)).all()
            for mentioned_user in mentioned_users:
                if mentioned_user.id != current_user.id:
                    create_notification(
                        mentioned_user.id,
                        f'{current_user.username} mentioned you on task "{task.title}"',
                        link=url_for('tasks.detail', task_id=task.id),
                    )

        # Notify task assignee
        if task.assigned_to and task.assigned_to != current_user.id:
            create_notification(task.assigned_to, f'New comment on task "{task.title}"', link=url_for('tasks.detail', task_id=task.id))
        flash('Comment posted', 'success')
    else:
        flash('Could not post comment', 'danger')
    return redirect(request.referrer or url_for('tasks.list_tasks'))


@comments_bp.route('/<int:comment_id>/seen', methods=['POST'])
@login_required
def mark_seen(comment_id):
    comment = db.get_or_404(Comment, comment_id)
    receipt = CommentReadReceipt.query.filter_by(comment_id=comment.id, user_id=current_user.id).first()
    if receipt is None:
        db.session.add(CommentReadReceipt(comment_id=comment.id, user_id=current_user.id))
        db.session.commit()
    return ('', 204)
