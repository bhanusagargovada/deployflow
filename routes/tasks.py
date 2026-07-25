from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from models.task import Task
from models.project import Project
from database import db
from forms.task_forms import TaskForm
from services.auth_service import record_activity
from utils.permissions import role_required
from models.user import Role

tasks_bp = Blueprint('tasks', __name__, url_prefix='/tasks', template_folder='../templates')


@tasks_bp.route('/')
@login_required
def list_tasks():
    q = request.args.get('q', type=str)
    status = request.args.get('status', type=str)
    assigned = request.args.get('assigned', type=int)
    page = request.args.get('page', default=1, type=int)
    per_page = request.args.get('per_page', default=10, type=int)

    query = Task.query
    if q:
        query = query.filter(Task.title.ilike(f'%{q}%'))
    if status:
        query = query.filter(Task.status == status)
    if assigned:
        query = query.filter(Task.assigned_to == assigned)

    from utils.pagination import paginate
    page_data = paginate(query.order_by(Task.created_at.desc()), page, per_page)
    return render_template('tasks/list.html', **page_data)


@tasks_bp.route('/create', methods=['GET', 'POST'])
@role_required([Role.ADMIN, Role.PM])
def create_task():
    form = TaskForm()
    if form.validate_on_submit():
        t = Task(title=form.title.data, description=form.description.data,
                 priority=form.priority.data, deadline=form.deadline.data,
                 assigned_to=form.assigned_to.data, progress=form.progress.data)
        db.session.add(t)
        db.session.commit()
        record_activity(current_user, 'create_task', meta=str({'task_id': t.id}))
        flash('Task created', 'success')
        return redirect(url_for('tasks.list_tasks'))
    return render_template('tasks/add.html', form=form)


@tasks_bp.route('/<int:task_id>')
@login_required
def detail(task_id):
    t = Task.query.get_or_404(task_id)
    # load comments
    from models.comment import Comment
    page = request.args.get('page', default=1, type=int)
    per_page = request.args.get('per_page', default=5, type=int)
    from utils.pagination import paginate
    comment_query = Comment.query.filter_by(task_id=t.id, parent_id=None).order_by(Comment.created_at.asc())
    page_data = paginate(comment_query, page, per_page)
    comments = page_data['items']
    from forms.comment_forms import CommentForm
    form = CommentForm()
    form.task_id.data = t.id
    return render_template('tasks/detail.html', task=t, comments=comments, form=form, **page_data)
