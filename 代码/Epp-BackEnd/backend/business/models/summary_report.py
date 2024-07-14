"""
综述报告表
"""
from django.db import models
import uuid

from .user import User


class SummaryReport(models.Model):
    """
    Field:
        - report_id          报告ID
        - user_id            用户ID
        - report_path        综述报告文件地址
        - title              综述报告title
        - date               时间
        - status             是否已经生成
    """
    STATUS_PENDING = 'P'
    STATUS_IN_PROGRESS = 'IP'
    STATUS_COMPLETED = 'C'
    STATUS_CHOICES = [
        (STATUS_PENDING, '未生成'),
        (STATUS_IN_PROGRESS, '生成中'),
        (STATUS_COMPLETED, '已生成'),
    ]

    report_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    report_path = models.CharField(max_length=255, unique=True)
    title = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=2,
        choices=STATUS_CHOICES,
        default=STATUS_COMPLETED,
    )
