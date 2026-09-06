from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from wtforms import HiddenField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, Optional


class CommentForm(FlaskForm):
    task_id = HiddenField('Task ID')
    parent_id = HiddenField('Parent ID')
    content = TextAreaField('Comment', validators=[DataRequired(), Length(min=1, max=2000)])
    attachment = FileField('Attachment', validators=[Optional(), FileAllowed(['png', 'jpg', 'jpeg', 'gif', 'pdf', 'txt', 'doc', 'docx'], 'Unsupported file type')])
    submit = SubmitField('Post')
