"""
通知表
"""
from django.db import models
from .user import User
import uuid


class Notification(models.Model):
    """
    Field:
        - notification_id       通知ID
        - user_id               用户ID
        - title                 通知标题
        - date                  通知时间
        - content               通知内容
        - is_read               是否已读
    """
    notification_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    is_read = models.BooleanField(default=False)
