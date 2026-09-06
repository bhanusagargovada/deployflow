from models.comment import Comment
from models.notification import Notification
import io

def test_comment_model_smoke():
    c = Comment(task_id=1, user_id=1, content='Hello', attachment_path='/static/uploads/comments/file.txt')
    assert c.content == 'Hello'
    assert c.message == 'Hello'
    assert c.attachment_path.endswith('file.txt')

def test_notification_model_smoke():
    n = Notification(user_id=1, message='Test', link='/')
    assert n.message == 'Test'
