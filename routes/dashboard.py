from flask import Blueprint, render_template
from flask_login import login_required
from models.project import Project, ProjectStatus
from models.task import Task, TaskStatus
from models.user import User

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/', template_folder='../templates')


@dashboard_bp.route('/')
@login_required
def index():
    stats = {
        'total_projects': Project.query.count(),
        'active_projects': Project.query.filter_by(status=ProjectStatus.ACTIVE).count(),
        'completed_projects': Project.query.filter_by(status=ProjectStatus.COMPLETED).count(),
        'pending_tasks': Task.query.filter(Task.status.in_([TaskStatus.TODO, TaskStatus.IN_PROGRESS])).count(),
        'completed_tasks': Task.query.filter_by(status=TaskStatus.DONE).count(),
        'total_users': User.query.count(),
    }
    return render_template('dashboard.html', stats=stats)
