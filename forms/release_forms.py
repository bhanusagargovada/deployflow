from flask_wtf import FlaskForm
from wtforms import StringField, DateField, TextAreaField, SelectField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Optional


class ReleaseForm(FlaskForm):
    version = StringField('Version', validators=[DataRequired()])
    release_date = DateField('Release Date', validators=[Optional()])
    notes = TextAreaField('Release Notes', validators=[Optional()])
    status = SelectField('Status', choices=[('Success','Success'),('Failed','Failed'),('Rollback','Rollback')])
    released_by = IntegerField('Released By (User ID)', validators=[Optional()])
    submit = SubmitField('Save')
