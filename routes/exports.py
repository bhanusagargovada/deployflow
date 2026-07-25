from flask import Blueprint, send_file, request
from flask_login import login_required
from io import StringIO
import csv
from models.project import Project
from models.task import Task
from utils.permissions import role_required
from models.user import Role

exports_bp = Blueprint('exports', __name__, url_prefix='/exports', template_folder='../templates')


@exports_bp.route('/projects.csv')
@login_required
@role_required([Role.ADMIN, Role.PM])
def projects_csv():
    projects = Project.query.order_by(Project.created_at.desc()).all()
    si = StringIO()
    cw = csv.writer(si)
    cw.writerow(['id', 'name', 'status', 'priority', 'deadline', 'manager_id', 'created_at'])
    for p in projects:
        cw.writerow([p.id, p.name, p.status, p.priority, p.deadline, p.manager_id, p.created_at])
    si.seek(0)
    return send_file(si, mimetype='text/csv', download_name='projects.csv', as_attachment=True)


@exports_bp.route('/tasks.csv')
@login_required
@role_required([Role.ADMIN, Role.PM])
def tasks_csv():
    tasks = Task.query.order_by(Task.created_at.desc()).all()
    si = StringIO()
    cw = csv.writer(si)
    cw.writerow(['id', 'title', 'status', 'priority', 'progress', 'project_id', 'assigned_to', 'created_at'])
    for t in tasks:
        cw.writerow([t.id, t.title, t.status, t.priority, t.progress, t.project_id, t.assigned_to, t.created_at])
    si.seek(0)
    return send_file(si, mimetype='text/csv', download_name='tasks.csv', as_attachment=True)
