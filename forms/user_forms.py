from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, Length, Optional


class UserCreateForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(3, 64)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(6)])
    role = SelectField('Role', choices=[('Administrator','Administrator'),('Project Manager','Project Manager'),('Team Member','Team Member')])
    submit = SubmitField('Create User')


class UserEditForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(3, 64)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    role = SelectField('Role', choices=[('Administrator','Administrator'),('Project Manager','Project Manager'),('Team Member','Team Member')])
    is_active = BooleanField('Is Active')
    submit = SubmitField('Save')
