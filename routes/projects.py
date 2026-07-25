from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from models.project import Project
from database import db
from forms.project_forms import ProjectForm
from services.auth_service import record_activity
from utils.permissions import role_required
from models.user import Role
from utils.pagination import paginate

projects_bp = Blueprint('projects', __name__, url_prefix='/projects', template_folder='../templates')


@projects_bp.route('/')
@login_required
def list_projects():
    q = request.args.get('q', type=str)
    status = request.args.get('status', type=str)
    priority = request.args.get('priority', type=str)
    manager = request.args.get('manager', type=int)
    page = request.args.get('page', default=1, type=int)
    per_page = request.args.get('per_page', default=10, type=int)

    query = Project.query
    if q:
        query = query.filter(Project.name.ilike(f'%{q}%'))
    if status:
        query = query.filter(Project.status == status)
    if priority:
        query = query.filter(Project.priority == priority)
    if manager:
        query = query.filter(Project.manager_id == manager)

    page_data = paginate(query.order_by(Project.created_at.desc()), page, per_page)
    return render_template('projects/list.html', **page_data)


@projects_bp.route('/create', methods=['GET', 'POST'])
@role_required([Role.ADMIN, Role.PM])
def create_project():
    form = ProjectForm()
    if form.validate_on_submit():
        p = Project(name=form.name.data, description=form.description.data,
                    priority=form.priority.data, deadline=form.deadline.data,
                    status=form.status.data, manager_id=current_user.id)
        db.session.add(p)
        db.session.commit()
        record_activity(current_user, 'create_project', meta=str({'project_id': p.id}))
        flash('Project created', 'success')
        return redirect(url_for('projects.list_projects'))
    return render_template('projects/add.html', form=form)


@projects_bp.route('/<int:project_id>/edit', methods=['GET', 'POST'])
@role_required([Role.ADMIN, Role.PM])
def edit_project(project_id):
    p = Project.query.get_or_404(project_id)
    form = ProjectForm(obj=p)
    if form.validate_on_submit():
        form.populate_obj(p)
        db.session.commit()
        flash('Project updated', 'success')
        return redirect(url_for('projects.list_projects'))
    return render_template('projects/edit.html', form=form, project=p)


@projects_bp.route('/<int:project_id>/delete', methods=['POST'])
@role_required([Role.ADMIN, Role.PM])
def delete_project(project_id):
    p = Project.query.get_or_404(project_id)
    db.session.delete(p)
    db.session.commit()
    flash('Project deleted', 'info')
    return redirect(url_for('projects.list_projects'))
