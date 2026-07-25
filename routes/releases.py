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
    if form.validate_on_submit():
        r = Release(version=form.version.data, release_date=form.release_date.data,
                    notes=form.notes.data, status=form.status.data,
                    released_by=form.released_by.data)
        db.session.add(r)
        db.session.commit()
        record_activity(current_user, 'create_release', meta=str({'release_id': r.id}))
        flash('Release recorded', 'success')
        return redirect(url_for('releases.list_releases'))
    return render_template('releases/add.html', form=form)
