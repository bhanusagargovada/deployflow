from flask import Blueprint, render_template
from flask_login import login_required

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/', template_folder='../templates')


@dashboard_bp.route('/')
@login_required
def index():
    # Placeholder summary data; real implementation will query models
    stats = {
        'total_projects': 0,
        'active_projects': 0,
        'completed_projects': 0,
        'pending_tasks': 0,
        'completed_tasks': 0,
        'total_users': 0,
    }
    return render_template('dashboard.html', stats=stats)
