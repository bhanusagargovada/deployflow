from flask_wtf import FlaskForm
from wtforms import StringField, DateField, TextAreaField, SelectField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Optional


class ReleaseForm(FlaskForm):
    project_id = SelectField('Project', coerce=int, validators=[DataRequired(message='Please select a project.')])
    version = StringField('Version', validators=[DataRequired()])
    release_date = DateField('Release Date', validators=[Optional()])
    notes = TextAreaField('Release Notes', validators=[Optional()])
    status = SelectField('Status', choices=[('Success','Success'),('Failed','Failed'),('Rollback','Rollback')])
    submit = SubmitField('Save')
