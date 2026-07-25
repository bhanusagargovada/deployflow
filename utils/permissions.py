from functools import wraps
from flask import abort, redirect, url_for, flash
from flask_login import current_user, login_required


def admin_required(f):
    @wraps(f)
    @login_required
    def decorated(*args, **kwargs):
        if not current_user.is_authenticated or not getattr(current_user, 'is_admin', lambda: False)():
            flash('Administrator access required.', 'danger')
            return redirect(url_for('dashboard.index'))
        return f(*args, **kwargs)

    return decorated


def role_required(roles):
    """Require the current_user to have one of the given role names.

    Roles may be a single string or an iterable of strings. Administrator
    always bypasses the check.
    """
    if isinstance(roles, str):
        allowed = {roles}
    else:
        allowed = set(roles)

    def decorator(f):
        @wraps(f)
        @login_required
        def decorated(*args, **kwargs):
            if not current_user.is_authenticated:
                flash('Access denied.', 'danger')
                return redirect(url_for('auth.login'))
            # Admins bypass role checks
            try:
                is_admin = getattr(current_user, 'is_admin', lambda: False)()
            except Exception:
                is_admin = False
            if is_admin:
                return f(*args, **kwargs)
            if getattr(current_user, 'role', None) not in allowed:
                flash('Insufficient permissions.', 'danger')
                return redirect(url_for('dashboard.index'))
            return f(*args, **kwargs)

        return decorated

    return decorator
