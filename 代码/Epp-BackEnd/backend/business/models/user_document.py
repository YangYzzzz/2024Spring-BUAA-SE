"""
用户上传文件表
"""
from django.db import models
import uuid

from .user import User


class UserDocument(models.Model):
    """
    Field:
        - document_id       文件ID
        - user_id           用户ID
        - title             文件标题
        - local_path        本地地址
        - upload_date       上传时间
        - format            文件格式
        - size              文件大小
    """
    document_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    local_path = models.CharField(max_length=255)
    upload_date = models.DateTimeField(auto_now_add=True)
    format = models.CharField(max_length=50)
    size = models.IntegerField()  # 文件大小以字节为单位

    def __str__(self):
        return self.title

    def get_document_id(self):
        return str(self.document_id)