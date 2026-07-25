from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, DateField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Optional, NumberRange


class TaskForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[Optional()])
    priority = SelectField('Priority', choices=[('Low','Low'),('Medium','Medium'),('High','High')])
    deadline = DateField('Deadline', validators=[Optional()])
    assigned_to = IntegerField('Assign To (User ID)', validators=[Optional()])
    progress = IntegerField('Progress', validators=[Optional(), NumberRange(0,100)])
    submit = SubmitField('Save')
