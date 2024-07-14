"""
数据库文献评分表
"""
from django.core.validators import MinValueValidator
from django.core.validators import MaxValueValidator
from django.db import models

from .paper import Paper
from .user import User


class PaperScore(models.Model):
    """
    Field:
        - user_id         用户ID
        - paper_id        文献ID
        - score           评分
    """
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    paper_id = models.ForeignKey(Paper, on_delete=models.CASCADE)
    score = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(10)])  # 评分限制在0到10之间

    class Meta:
        unique_together = [['user_id', 'paper_id']]
