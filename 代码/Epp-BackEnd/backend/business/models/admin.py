"""
管理员表
"""
from django.db import models
import uuid


class Admin(models.Model):
    """
    Field:
        - admin_id          管理员ID
        - admin_name        管理员名
        - password          密码
    """
    admin_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    admin_name = models.CharField(max_length=64)
    password = models.CharField(max_length=128)

    def __str__(self):
        return self.admin_name
