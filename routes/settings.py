from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user

settings_bp = Blueprint('settings', __name__, url_prefix='/settings', template_folder='../templates')


@settings_bp.route('/', methods=['GET', 'POST'])
@login_required
def index():
    if request.method == 'POST':
        # placeholder for user settings: theme, notifications
        flash('DeployFlow settings saved', 'success')
        return redirect(url_for('settings.index'))
    return render_template('settings/index.html')
