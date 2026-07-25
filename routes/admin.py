from flask import Blueprint, render_template, redirect, url_for, flash, request
from utils.permissions import admin_required
from database import db
from models.user import User
from models.activity import ActivityLog
from forms.user_forms import UserCreateForm, UserEditForm
from services.auth_service import record_activity

admin_bp = Blueprint('admin', __name__, url_prefix='/admin', template_folder='../templates')


@admin_bp.route('/')
@admin_required
def index():
    users = User.query.order_by(User.created_at.desc()).all()
    return render_template('admin/list.html', users=users)


@admin_bp.route('/create', methods=['GET', 'POST'])
@admin_required
def create_user():
    form = UserCreateForm()
    if form.validate_on_submit():
        u = User(username=form.username.data, email=form.email.data, role=form.role.data)
        u.set_password(form.password.data)
        db.session.add(u)
        db.session.commit()
        record_activity(None, f'admin_created_user:{u.id}', meta=str({'by': 'admin'}))
        flash('User created.', 'success')
        return redirect(url_for('admin.index'))
    return render_template('admin/create.html', form=form)


@admin_bp.route('/<int:user_id>/edit', methods=['GET', 'POST'])
@admin_required
def edit_user(user_id):
    u = User.query.get_or_404(user_id)
    form = UserEditForm(obj=u)
    if form.validate_on_submit():
        u.username = form.username.data
        u.email = form.email.data
        u.role = form.role.data
        u.is_active = bool(form.is_active.data)
        db.session.commit()
        record_activity(None, f'admin_updated_user:{u.id}')
        flash('User updated.', 'success')
        return redirect(url_for('admin.index'))
    return render_template('admin/edit.html', form=form, user=u)


@admin_bp.route('/<int:user_id>/delete', methods=['POST'])
@admin_required
def delete_user(user_id):
    u = User.query.get_or_404(user_id)
    db.session.delete(u)
    db.session.commit()
    record_activity(None, f'admin_deleted_user:{user_id}')
    flash('User deleted.', 'info')
    return redirect(url_for('admin.index'))


@admin_bp.route('/<int:user_id>/activity')
@admin_required
def user_activity(user_id):
    activities = ActivityLog.query.filter_by(user_id=user_id).order_by(ActivityLog.timestamp.desc()).all()
    return render_template('admin/activity.html', activities=activities)
