from datetime import datetime, timezone

from flask import Blueprint, flash, redirect, request, url_for
from flask_login import current_user, login_required

from database import db
from forms.collaboration_forms import (
    AnnouncementForm,
    ClarificationAnswerForm,
    ClarificationRequestForm,
    StatusReportForm,
    StatusReportReviewForm,
)
from models.announcement import Announcement
from models.clarification_request import ClarificationRequest, ClarificationStatus
from models.project import Project
from models.project_member import ProjectMember
from models.status_report import StatusReport, StatusReportStatus
from models.task import Task
from models.user import Role, User
from services.notification_service import create_notification
from utils.permissions import role_required

collaboration_bp = Blueprint('collaboration', __name__, url_prefix='/collaboration', template_folder='../templates')


def _task_or_404(task_id):
    return db.get_or_404(Task, task_id)


@collaboration_bp.route('/clarifications/create', methods=['POST'])
@login_required
def create_clarification_request():
    form = ClarificationRequestForm()
    if form.validate_on_submit():
        task = _task_or_404(form.task_id.data)
        assigned_to = task.project.manager_id if task.project and task.project.manager_id else task.assigned_to
        clarification = ClarificationRequest(
            task_id=task.id,
            raised_by=current_user.id,
            assigned_to=assigned_to,
            question=form.question.data,
        )
        db.session.add(clarification)
        db.session.commit()
        if assigned_to and assigned_to != current_user.id:
            create_notification(
                assigned_to,
                f'Clarification request on task "{task.title}"',
                link=url_for('tasks.detail', task_id=task.id),
            )
        flash('Clarification request sent.', 'success')
    else:
        flash('Could not send clarification request.', 'danger')
    return redirect(request.referrer or url_for('tasks.detail', task_id=form.task_id.data or 0))


@collaboration_bp.route('/clarifications/<int:request_id>/answer', methods=['POST'])
@login_required
@role_required([Role.ADMIN, Role.PM])
def answer_clarification_request(request_id):
    clarification = db.get_or_404(ClarificationRequest, request_id)
    form = ClarificationAnswerForm()
    if form.validate_on_submit():
        clarification.answer = form.answer.data
        clarification.status = ClarificationStatus.ANSWERED
        clarification.resolved_at = datetime.now(timezone.utc)
        db.session.commit()
        if clarification.raised_by != current_user.id:
            create_notification(
                clarification.raised_by,
                f'Clarification answered for task #{clarification.task_id}',
                link=url_for('tasks.detail', task_id=clarification.task_id),
            )
        flash('Clarification answered.', 'success')
    else:
        flash('Could not answer clarification request.', 'danger')
    return redirect(request.referrer or url_for('tasks.detail', task_id=clarification.task_id))


@collaboration_bp.route('/clarifications/<int:request_id>/close', methods=['POST'])
@login_required
def close_clarification_request(request_id):
    clarification = db.get_or_404(ClarificationRequest, request_id)
    if current_user.id not in {clarification.raised_by, clarification.assigned_to} and not current_user.is_admin() and current_user.role != Role.PM:
        return ('', 403)
    clarification.status = ClarificationStatus.CLOSED
    clarification.resolved_at = datetime.now(timezone.utc)
    db.session.commit()
    flash('Clarification closed.', 'info')
    return redirect(request.referrer or url_for('tasks.detail', task_id=clarification.task_id))


@collaboration_bp.route('/status-reports/create', methods=['POST'])
@login_required
def create_status_report():
    form = StatusReportForm()
    if form.validate_on_submit():
        project = db.get_or_404(Project, form.project_id.data)
        report = StatusReport(
            project_id=project.id,
            task_id=form.task_id.data or None,
            submitted_by=current_user.id,
            report_date=form.report_date.data,
            work_done=form.work_done.data,
            blockers=form.blockers.data,
            hours_spent=form.hours_spent.data,
            next_steps=form.next_steps.data,
        )
        db.session.add(report)
        db.session.commit()
        if project.manager_id and project.manager_id != current_user.id:
            create_notification(
                project.manager_id,
                f'New status report for project "{project.name}"',
                link=url_for('reports.index'),
            )
        flash('Status report submitted.', 'success')
    else:
        flash('Could not submit status report.', 'danger')
    return redirect(request.referrer or url_for('projects.list_projects'))


@collaboration_bp.route('/status-reports/<int:report_id>/review', methods=['POST'])
@login_required
@role_required([Role.ADMIN, Role.PM])
def review_status_report(report_id):
    report = db.get_or_404(StatusReport, report_id)
    form = StatusReportReviewForm()
    if form.validate_on_submit():
        report.status = form.status.data
        report.manager_feedback = form.manager_feedback.data
        report.reviewed_by = current_user.id
        report.reviewed_at = datetime.now(timezone.utc)
        db.session.commit()
        if report.submitted_by != current_user.id:
            create_notification(
                report.submitted_by,
                f'Status report for project #{report.project_id} was reviewed',
                link=url_for('reports.index'),
            )
        flash('Status report reviewed.', 'success')
    else:
        flash('Could not review status report.', 'danger')
    return redirect(request.referrer or url_for('reports.index'))


@collaboration_bp.route('/announcements/create', methods=['POST'])
@login_required
@role_required([Role.ADMIN, Role.PM])
def create_announcement():
    form = AnnouncementForm()
    if form.validate_on_submit():
        project = db.get_or_404(Project, form.project_id.data)
        if current_user.role == Role.PM and project.manager_id not in (None, current_user.id):
            return ('', 403)
        announcement = Announcement(
            project_id=project.id,
            posted_by=current_user.id,
            message=form.message.data,
            pinned=bool(form.pinned.data),
        )
        db.session.add(announcement)
        db.session.commit()
        recipients = {member.user_id for member in project.members}
        for user_id in recipients:
            if user_id != current_user.id:
                create_notification(user_id, f'New project announcement for "{project.name}"', link=url_for('projects.list_projects'))
        flash('Announcement posted.', 'success')
    else:
        flash('Could not post announcement.', 'danger')
    return redirect(request.referrer or url_for('projects.list_projects'))