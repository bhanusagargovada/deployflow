from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from database import db
from models.user import User
from forms.user_forms import UserEditForm

profile_bp = Blueprint('profile', __name__, url_prefix='/profile', template_folder='../templates')


@profile_bp.route('/')
@login_required
def view_profile():
    return render_template('profile/view.html', user=current_user)


@profile_bp.route('/edit', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = UserEditForm(obj=current_user)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Profile updated', 'success')
        return redirect(url_for('profile.view_profile'))
    return render_template('profile/edit.html', form=form)
