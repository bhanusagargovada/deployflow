from flask import Blueprint, request, redirect, url_for, flash, render_template
from flask_login import login_required, current_user
from forms.comment_forms import CommentForm
from database import db
from models.comment import Comment
from models.task import Task
from services.auth_service import record_activity
from services.notification_service import create_notification

comments_bp = Blueprint('comments', __name__, url_prefix='/comments', template_folder='../templates')


@comments_bp.route('/create', methods=['POST'])
@login_required
def create_comment():
    form = CommentForm()
    if form.validate_on_submit():
        task = Task.query.get(form.task_id.data)
        if not task:
            flash('Task not found', 'danger')
            return redirect(request.referrer or url_for('tasks.list_tasks'))
        c = Comment(task_id=task.id, user_id=current_user.id, parent_id=form.parent_id.data or None, content=form.content.data)
        db.session.add(c)
        db.session.commit()
        record_activity(current_user, 'create_comment', meta=str({'comment_id': c.id, 'task_id': task.id}))
        # Notify task assignee
        if task.assigned_to and task.assigned_to != current_user.id:
            create_notification(task.assigned_to, f'New comment on task "{task.title}"', link=url_for('tasks.detail', task_id=task.id))
        flash('Comment posted', 'success')
    else:
        flash('Could not post comment', 'danger')
    return redirect(request.referrer or url_for('tasks.list_tasks'))
