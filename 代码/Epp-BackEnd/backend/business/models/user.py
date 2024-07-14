"""
普通用户表
"""
from django.db import models
import uuid

from business.utils import storage
from .paper import Paper


class User(models.Model):
    """
    Field:
        - user_id             用户ID
        - username            用户名
        - password            密码
        - avatar              头像
        - registration_date   注册时间
        - collected_papers    收藏的文献
        - liked_papers        点赞的文献
    """
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    avatar = models.ImageField(
        upload_to=f'uploads/users/avatars/',
        default='uploads/users/avatars/default.jpg',
        storage=storage.ImageStorage(), null=True
    )
    registration_date = models.DateTimeField(auto_now_add=True)  # 自动设置为当前时间
    collected_papers = models.ManyToManyField(Paper, related_name='collected_by_users', blank=True)
    liked_papers = models.ManyToManyField(Paper, related_name='liked_by_users', blank=True)

    def __str__(self):
        return self.username

    def simply_desc(self):
        return {
            "user_id": str(self.user_id),
            "user_name": str(self.username)
        }
