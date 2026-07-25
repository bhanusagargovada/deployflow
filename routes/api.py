from flask import Blueprint, jsonify
from flask_login import login_required
from utils.permissions import role_required
from models.user import Role
from models.project import Project
from models.task import Task
from models.user import User
from database import db
from sqlalchemy import func

api_bp = Blueprint('api', __name__, url_prefix='/api')


@api_bp.route('/project_status')
@login_required
def project_status():
    q = db.session.query(Project.status, func.count(Project.id)).group_by(Project.status).all()
    data = {row[0]: row[1] for row in q}
    return jsonify(data)


@api_bp.route('/monthly_projects')
@login_required
def monthly_projects():
    q = db.session.query(func.month(Project.created_at), func.count(Project.id)).group_by(func.month(Project.created_at)).all()
    data = {str(int(row[0])): row[1] for row in q}
    return jsonify(data)


@api_bp.route('/task_completion')
@login_required
def task_completion():
    total = db.session.query(func.count(Task.id)).scalar() or 0
    done = db.session.query(func.count(Task.id)).filter(Task.status == 'Done').scalar() or 0
    return jsonify({'total': total, 'done': done})


@api_bp.route('/user_productivity')
@login_required
@role_required([Role.ADMIN, Role.PM])
def user_productivity():
    q = db.session.query(User.username, func.count(Task.id)).join(Task, Task.assigned_to == User.id).filter(Task.status == 'Done').group_by(User.id).all()
    data = [{'user': row[0], 'completed': row[1]} for row in q]
    return jsonify(data)
