from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from models.task import Task
from models.project import Project
from database import db
from forms.task_forms import TaskForm
from services.auth_service import record_activity
from utils.permissions import role_required
from models.user import Role, User
from models.project_member import ProjectMember
from sqlalchemy import or_

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

    if current_user.is_admin():
        allowed_projects = Project.query.order_by(Project.name.asc()).all()
    else:
        allowed_projects = Project.query.filter_by(manager_id=current_user.id).order_by(Project.name.asc()).all()

    if not allowed_projects:
        flash('No projects available. Please create a project first.', 'warning')
        return redirect(url_for('projects.list_projects'))

    form.project_id.choices = [(p.id, p.name) for p in allowed_projects]

    # Determine currently selected project
    selected_project_id = None
    if request.method == 'POST':
        selected_project_id = request.form.get('project_id', type=int)
    if not selected_project_id:
        req_pid = request.args.get('project_id', type=int)
        if req_pid and any(p.id == req_pid for p in allowed_projects):
            selected_project_id = req_pid
        elif allowed_projects:
            selected_project_id = allowed_projects[0].id

    if selected_project_id:
        form.project_id.data = selected_project_id

    # Populate assigned_to with active Team Members belonging to the selected project
    members = []
    if selected_project_id:
        members = (
            User.query.join(ProjectMember, ProjectMember.user_id == User.id)
            .filter(
                ProjectMember.project_id == selected_project_id,
                User.is_active == True,
                User.role == Role.MEMBER,
            )
            .order_by(User.username.asc())
            .all()
        )
    form.assigned_to.choices = [(0, 'Unassigned')] + [(m.id, f"{m.username} ({m.email})") for m in members]

    if form.validate_on_submit():
        project = db.session.get(Project, form.project_id.data)
        if not project:
            flash('Selected project does not exist.', 'danger')
            return render_template('tasks/add.html', form=form)

        # Rule 4 & 5: Project Managers may modify only projects they manage.
        if not current_user.is_admin() and project.manager_id != current_user.id:
            flash('Project Managers may modify only projects they manage.', 'danger')
            return redirect(url_for('tasks.list_tasks'))

        # Rule 3: A Task may only be assigned to an active Team Member who is a member of the selected Project.
        assigned_to_id = form.assigned_to.data if form.assigned_to.data and form.assigned_to.data > 0 else None
        if assigned_to_id:
            is_valid_member = (
                User.query.join(ProjectMember, ProjectMember.user_id == User.id)
                .filter(
                    ProjectMember.project_id == project.id,
                    User.id == assigned_to_id,
                    User.is_active == True,
                    User.role == Role.MEMBER,
                )
                .first()
            )
            if not is_valid_member:
                flash('A Task may only be assigned to an active Team Member who is a member of the selected Project.', 'danger')
                return render_template('tasks/add.html', form=form)

        t = Task(
            title=form.title.data,
            description=form.description.data,
            priority=form.priority.data,
            deadline=form.deadline.data,
            project_id=project.id,
            assigned_to=assigned_to_id,
            progress=form.progress.data or 0,
        )
        db.session.add(t)
        db.session.commit()
        record_activity(current_user, 'create_task', meta=str({'task_id': t.id, 'project_id': project.id}))
        flash('Task created', 'success')
        return redirect(url_for('tasks.list_tasks'))

    return render_template('tasks/add.html', form=form)


@tasks_bp.route('/<int:task_id>')
@login_required
def detail(task_id):
    t = db.get_or_404(Task, task_id)
    # load comments
    from models.comment import Comment, CommentReadReceipt
    from models.clarification_request import ClarificationRequest
    from models.status_report import StatusReport
    from models.announcement import Announcement
    page = request.args.get('page', default=1, type=int)
    per_page = request.args.get('per_page', default=5, type=int)
    from utils.pagination import paginate
    comment_query = Comment.query.filter_by(task_id=t.id, parent_id=None).order_by(Comment.created_at.asc())
    page_data = paginate(comment_query, page, per_page)
    comments = page_data['items']
    for comment in comments:
        if not comment.seen_by(current_user.id):
            db.session.add(CommentReadReceipt(comment_id=comment.id, user_id=current_user.id))
    db.session.commit()

    clarification_requests = ClarificationRequest.query.filter_by(task_id=t.id).order_by(ClarificationRequest.created_at.desc()).all()
    status_reports = []
    if t.project_id:
        status_reports = StatusReport.query.filter(
            or_(StatusReport.project_id == t.project_id, StatusReport.task_id == t.id)
        ).order_by(StatusReport.report_date.desc()).all()
    announcements = Announcement.query.filter_by(project_id=t.project_id).order_by(Announcement.pinned.desc(), Announcement.created_at.desc()).all() if t.project_id else []

    from forms.comment_forms import CommentForm
    from forms.collaboration_forms import (
        AnnouncementForm,
        ClarificationAnswerForm,
        ClarificationRequestForm,
        StatusReportForm,
        StatusReportReviewForm,
    )

    comment_form = CommentForm()
    comment_form.task_id.data = t.id

    clarification_form = ClarificationRequestForm()
    clarification_form.task_id.data = t.id

    status_report_form = StatusReportForm()
    status_report_form.project_id.data = t.project_id or ''
    status_report_form.task_id.data = t.id

    announcement_form = AnnouncementForm()
    announcement_form.project_id.data = t.project_id or ''

    review_form = StatusReportReviewForm()
    answer_form = ClarificationAnswerForm()

    return render_template(
        'tasks/detail.html',
        task=t,
        comments=comments,
        form=comment_form,
        clarification_form=clarification_form,
        clarification_answer_form=answer_form,
        clarification_requests=clarification_requests,
        status_report_form=status_report_form,
        review_form=review_form,
        status_reports=status_reports,
        announcement_form=announcement_form,
        announcements=announcements,
        **page_data,
    )
