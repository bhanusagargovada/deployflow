from flask import Blueprint, render_template, send_file, abort
from flask_login import login_required
from models.project import Project
from models.task import Task
from models.release import Release
from services.pdf_service import generate_project_report

from services.pdf_service import generate_task_report, generate_release_report
from utils.permissions import role_required
from models.user import Role

reports_bp = Blueprint('reports', __name__, url_prefix='/reports', template_folder='../templates')


@reports_bp.route('/')
@login_required
def index():
    return render_template('reports/list.html')


@reports_bp.route('/project/<int:project_id>/pdf')
@login_required
@role_required([Role.ADMIN, Role.PM])
def project_pdf(project_id):
    project = Project.query.get_or_404(project_id)
    tasks = Task.query.filter_by(project_id=project.id).all()
    releases = Release.query.filter_by(project_id=project.id).all()
    buf = generate_project_report(project, tasks=tasks, releases=releases)
    return send_file(buf, mimetype='application/pdf', download_name=f'project_{project.id}_report.pdf', as_attachment=True)


@reports_bp.route('/task/<int:task_id>/pdf')
@login_required
@role_required([Role.ADMIN, Role.PM])
def task_pdf(task_id):
    task = Task.query.get_or_404(task_id)
    buf = generate_task_report(task)
    return send_file(buf, mimetype='application/pdf', download_name=f'task_{task.id}_report.pdf', as_attachment=True)


@reports_bp.route('/release/<int:release_id>/pdf')
@login_required
@role_required([Role.ADMIN, Role.PM])
def release_pdf(release_id):
    release = Release.query.get_or_404(release_id)
    buf = generate_release_report(release)
    return send_file(buf, mimetype='application/pdf', download_name=f'release_{release.id}_report.pdf', as_attachment=True)
