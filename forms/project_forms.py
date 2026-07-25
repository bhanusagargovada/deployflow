from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, DateField, SubmitField
from wtforms.validators import DataRequired, Length, Optional


class ProjectForm(FlaskForm):
    name = StringField('Project Name', validators=[DataRequired(), Length(max=140)])
    description = TextAreaField('Description', validators=[Optional()])
    priority = SelectField('Priority', choices=[('Low','Low'),('Medium','Medium'),('High','High')])
    deadline = DateField('Deadline', validators=[Optional()])
    status = SelectField('Status', choices=[('Planned','Planned'),('Active','Active'),('Completed','Completed'),('On Hold','On Hold')])
    submit = SubmitField('Save')
