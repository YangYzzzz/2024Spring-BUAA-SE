"""
用户搜索记录表
"""
from django.db import models
import uuid

from .user import User
from .paper import Paper


class SearchRecord(models.Model):
    """
    Field:
        - search_record_id      搜素记录ID
        - user_id               用户ID
        - keyword               搜索关键字
        - date                  搜索时间
        - conservation_path     对话文件地址
        - related_papers        相关论文
    """
    search_record_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    keyword = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now=True)
    conversation_path = models.CharField(max_length=255, null=True)
    related_papers = models.ManyToManyField(Paper, related_name='related_search_record', blank=True)
