from flask_wtf import FlaskForm
from wtforms import TextAreaField, HiddenField, SubmitField
from wtforms.validators import DataRequired, Length


class CommentForm(FlaskForm):
    task_id = HiddenField('Task ID')
    parent_id = HiddenField('Parent ID')
    content = TextAreaField('Comment', validators=[DataRequired(), Length(min=1, max=2000)])
    submit = SubmitField('Post')
