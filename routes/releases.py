from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from models.release import Release
from models.project import Project
from database import db
from forms.release_forms import ReleaseForm
from services.auth_service import record_activity
from utils.permissions import role_required
from models.user import Role

releases_bp = Blueprint('releases', __name__, url_prefix='/releases', template_folder='../templates')


@releases_bp.route('/')
@login_required
def list_releases():
    releases = Release.query.all()
    return render_template('releases/list.html', releases=releases)


@releases_bp.route('/create', methods=['GET', 'POST'])
@role_required([Role.ADMIN, Role.PM])
def create_release():
    form = ReleaseForm()

    if current_user.is_admin():
        allowed_projects = Project.query.order_by(Project.name.asc()).all()
    else:
        allowed_projects = Project.query.filter_by(manager_id=current_user.id).order_by(Project.name.asc()).all()

    if not allowed_projects:
        flash('No projects available. Please create a project first.', 'warning')
        return redirect(url_for('projects.list_projects'))

    form.project_id.choices = [(p.id, p.name) for p in allowed_projects]

    req_pid = request.args.get('project_id', type=int)
    if req_pid and any(p.id == req_pid for p in allowed_projects) and request.method == 'GET':
        form.project_id.data = req_pid

    if form.validate_on_submit():
        project = db.session.get(Project, form.project_id.data)
        if not project:
            flash('Selected project does not exist.', 'danger')
            return render_template('releases/add.html', form=form)

        # Rule 4 & 5: Project Managers may modify only projects they manage.
        if not current_user.is_admin() and project.manager_id != current_user.id:
            flash('Project Managers may modify only projects they manage.', 'danger')
            return redirect(url_for('releases.list_releases'))

        r = Release(
            project_id=project.id,
            version=form.version.data,
            release_date=form.release_date.data,
            notes=form.notes.data,
            status=form.status.data,
            released_by=current_user.id,
        )
        db.session.add(r)
        db.session.commit()
        record_activity(current_user, 'create_release', meta=str({'release_id': r.id, 'project_id': project.id}))
        flash('Release recorded', 'success')
        return redirect(url_for('releases.list_releases'))

    return render_template('releases/add.html', form=form)
