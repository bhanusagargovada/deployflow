from flask_wtf import FlaskForm
from wtforms import BooleanField, DateField, FloatField, HiddenField, SelectField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Optional, NumberRange


class ClarificationRequestForm(FlaskForm):
    task_id = HiddenField('Task ID')
    question = TextAreaField('Clarification Request', validators=[DataRequired()])
    submit = SubmitField('Send Request')


class ClarificationAnswerForm(FlaskForm):
    answer = TextAreaField('Answer', validators=[DataRequired()])
    submit = SubmitField('Submit Answer')


class StatusReportForm(FlaskForm):
    project_id = HiddenField('Project ID')
    task_id = HiddenField('Task ID')
    report_date = DateField('Report Date', validators=[Optional()])
    work_done = TextAreaField('Work Done', validators=[DataRequired()])
    blockers = TextAreaField('Blockers', validators=[Optional()])
    hours_spent = FloatField('Hours Spent', validators=[Optional(), NumberRange(min=0)])
    next_steps = TextAreaField('Next Steps', validators=[Optional()])
    submit = SubmitField('Submit Report')


class StatusReportReviewForm(FlaskForm):
    status = SelectField('Status', choices=[('Approved', 'Approved'), ('ChangesRequested', 'Request Changes'), ('Rejected', 'Reject')])
    manager_feedback = TextAreaField('Feedback', validators=[Optional()])
    submit = SubmitField('Review Report')


class AnnouncementForm(FlaskForm):
    project_id = HiddenField('Project ID')
    message = TextAreaField('Announcement', validators=[DataRequired()])
    pinned = BooleanField('Pin to project feed')
    submit = SubmitField('Post Announcement')