"""
文献评论表：一级评论表、二级评论表
"""
from django.db import models
import uuid

from .user import User
from .paper import Paper


class FirstLevelComment(models.Model):
    """
    Field:
        - comment_id         评论ID
        - user_id            用户ID
        - paper_id           文献ID
        - date               评论时间
        - text               评论内容
        - like_count         点赞数
        - liked_by_users     点赞用户
        - visibility         可见性
    """
    comment_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    paper_id = models.ForeignKey(Paper, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    text = models.TextField()
    like_count = models.IntegerField(default=0)
    liked_by_users = models.ManyToManyField(User, related_name='liked_first_level_comments', blank=True)
    visibility = models.BooleanField(default=True)


class SecondLevelComment(models.Model):
    """
    Field:
        - comment_id         评论ID
        - user_id            用户ID
        - paper_id           文献ID
        - date               评论时间
        - text               评论内容
        - like_count         点赞数
        - level1_comment     一级评论
        - reply_comment      回复评论(针对二级评论的回复才记录）
        - liked_by_users     点赞用户
        - visibility         可见性
    """
    comment_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    paper_id = models.ForeignKey(Paper, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    text = models.TextField()
    like_count = models.IntegerField(default=0)
    level1_comment = models.ForeignKey(FirstLevelComment, on_delete=models.CASCADE)
    reply_comment = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    liked_by_users = models.ManyToManyField(User, related_name='liked_second_level_comments', blank=True)
    visibility = models.BooleanField(default=True)
