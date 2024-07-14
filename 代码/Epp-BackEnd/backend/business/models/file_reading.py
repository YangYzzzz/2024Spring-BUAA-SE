"""
用户论文研读记录表
"""
from django.db import models

from .user import User
from .paper import Paper
from .user_document import UserDocument


class FileReading(models.Model):
    """
    Field:
        - user_id               用户ID
        - document_id           用户文件ID
        - paper_id              论文ID
        - title                 研读标题
        - conversation_path     对话记录文件地址
        - date                  最近研读时间
    """
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    document_id = models.ForeignKey(UserDocument, on_delete=models.CASCADE, null=True, blank=True)
    paper_id = models.ForeignKey(Paper, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=255)
    conversation_path = models.CharField(max_length=255, null=True)
    date = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = [['user_id', 'conversation_path']]
