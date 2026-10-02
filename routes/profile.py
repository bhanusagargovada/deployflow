from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from database import db
from models.user import User
from models.task import Task
from forms.user_forms import UserEditForm

profile_bp = Blueprint(
    'profile',
    __name__,
    url_prefix='/profile',
    template_folder='../templates'
)


@profile_bp.route('/')
@login_required
def view_profile():

    # Count tasks completed by the logged-in user
    completed_tasks = Task.query.filter_by(
        assigned_to=current_user.id,
        status='Done'
    ).count()

    # Achievement badges
    badges = []

    if completed_tasks >= 1:
        badges.append({
            'name': 'First Task',
            'icon': '🏅',
            'description': 'Completed your first task'
        })

    if completed_tasks >= 5:
        badges.append({
            'name': 'Task Starter',
            'icon': '⭐',
            'description': 'Completed 5 tasks'
        })

    if completed_tasks >= 10:
        badges.append({
            'name': 'Task Champion',
            'icon': '🏆',
            'description': 'Completed 10 tasks'
        })

    if completed_tasks >= 20:
        badges.append({
            'name': 'Productive Member',
            'icon': '🚀',
            'description': 'Completed 20 tasks'
        })

    return render_template(
        'profile/view.html',
        user=current_user,
        completed_tasks=completed_tasks,
        badges=badges
    )


@profile_bp.route('/edit', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = UserEditForm(obj=current_user)

    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()

        flash('DeployFlow profile updated', 'success')
        return redirect(url_for('profile.view_profile'))

    return render_template('profile/edit.html', form=form)