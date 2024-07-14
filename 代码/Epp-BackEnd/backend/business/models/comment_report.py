"""
举报审核表
"""
from django.db import models

from .user import User
from .comment import FirstLevelComment, SecondLevelComment


class CommentReport(models.Model):
    """
    Field:
        - comment_id_1       一级评论ID
        - comment_id_2       二级评论ID
        - comment_level      评论级别
        - user_id            用户ID
        - date               举报时间
        - content            举报内容
        - judgment           处理意见
        - processed          举报完成情况
    """
    comment_id_1 = models.ForeignKey(FirstLevelComment, on_delete=models.CASCADE, null=True, blank=True)
    comment_id_2 = models.ForeignKey(SecondLevelComment, on_delete=models.CASCADE, null=True, blank=True)
    comment_level = models.IntegerField(default=1)  # 1代表一级评论，2代表二级评论
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    content = models.TextField(null=True, blank=True)
    judgment = models.TextField(null=True, blank=True)
    processed = models.BooleanField(default=False)
