from flask import Blueprint, render_template, redirect, url_for, flash, request
from forms.auth_forms import LoginForm, RegistrationForm, ForgotPasswordForm, ResetPasswordForm
from database import db
from models.user import User, Role
from flask_login import login_user, logout_user, current_user, login_required
from utils.token_utils import generate_token, verify_token
from utils.email_utils import send_email

auth_bp = Blueprint('auth', __name__, url_prefix='/auth', template_folder='../templates')


ROLE_PORTALS = {
    'admin': {
        'slug': 'admin',
        'role': Role.ADMIN,
        'title': 'Administrator Login',
        'subtitle': 'Manage users, projects, reports and system settings.',
        'action': 'auth.admin_login',
        'icon': 'bi-shield-lock-fill',
        'accent': 'portal-admin',
    },
    'pm': {
        'slug': 'pm',
        'role': Role.PM,
        'title': 'Project Manager Login',
        'subtitle': 'Create projects, assign tasks and monitor progress.',
        'action': 'auth.pm_login',
        'icon': 'bi-clipboard-data-fill',
        'accent': 'portal-pm',
    },
    'member': {
        'slug': 'member',
        'role': Role.MEMBER,
        'title': 'Team Member Login',
        'subtitle': 'View assigned tasks, update progress and upload work.',
        'action': 'auth.member_login',
        'icon': 'bi-people-fill',
        'accent': 'portal-member',
    },
}


def _render_login_page(active_portal_slug=None, form=None):
    active_portal = ROLE_PORTALS.get(active_portal_slug)
    login_cards = [
        {
            **portal,
            'action_url': url_for(portal['action']),
        }
        for portal in ROLE_PORTALS.values()
    ]
    return render_template(
        'auth/login.html',
        form=form or LoginForm(),
        login_cards=login_cards,
        active_portal=active_portal,
    )


def _handle_role_login(role_key=None):
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))

    form = LoginForm()
    portal = ROLE_PORTALS.get(role_key) if role_key else None
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        role_is_allowed = user and (not portal or user.role == portal['role'])
        if role_is_allowed and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            flash('Logged in successfully', 'success')
            next_page = request.args.get('next')
            return redirect(next_page or url_for('dashboard.index'))
        flash('Invalid credentials.', 'danger')

    return _render_login_page(active_portal_slug=role_key if portal else None, form=form)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    return _handle_role_login()


@auth_bp.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    return _handle_role_login('admin')


@auth_bp.route('/pm/login', methods=['GET', 'POST'])
def pm_login():
    return _handle_role_login('pm')


@auth_bp.route('/member/login', methods=['GET', 'POST'])
def member_login():
    return _handle_role_login('member')


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Account created. You can now sign in to DeployFlow.', 'success')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)


@auth_bp.route('/forgot', methods=['GET', 'POST'])
def forgot_password():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))
    form = ForgotPasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            token = generate_token(user.email)
            reset_url = url_for('auth.reset_password', token=token, _external=True)
            body = f'Hello {user.username},\n\nTo reset your password, click the link below:\n{reset_url}\n\nIf you did not request this, ignore this email.'
            send_email('DeployFlow Password Reset', [user.email], body)
            flash('If the email exists, a DeployFlow reset link has been sent.', 'info')
        else:
            flash('If the email exists, a DeployFlow reset link has been sent.', 'info')
        return redirect(url_for('auth.login'))
    return render_template('auth/forgot.html', form=form)


@auth_bp.route('/reset/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))
    email = verify_token(token)
    if not email:
        flash('The DeployFlow reset link is invalid or has expired.', 'danger')
        return redirect(url_for('auth.forgot_password'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=email).first()
        if user:
            user.set_password(form.password.data)
            db.session.commit()
            flash('Your DeployFlow password has been reset. Please log in.', 'success')
            return redirect(url_for('auth.login'))
        else:
            flash('DeployFlow user not found.', 'danger')
            return redirect(url_for('auth.register'))
    return render_template('auth/reset.html', form=form)


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out', 'info')
    return redirect(url_for('auth.login'))
