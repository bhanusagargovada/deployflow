from models.comment import Comment
from models.notification import Notification
import io

def test_comment_model_smoke():
    c = Comment(task_id=1, user_id=1, content='Hello')
    assert c.content == 'Hello'

def test_notification_model_smoke():
    n = Notification(user_id=1, message='Test', link='/')
    assert n.message == 'Test'
