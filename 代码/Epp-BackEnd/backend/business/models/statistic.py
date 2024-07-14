"""
数据库统计
"""
from django.db import models


class UserDailyAddition(models.Model):
    """
    Field:
        - date          时间
        - addition      用户新增
    """
    date = models.DateField(auto_now=True)
    addition = models.IntegerField(default=0)


class UserVisit(models.Model):
    """
    Field:
        - ip_address    客户端 ip 地址
        - timestamp     访问时间
    """
    ip_address = models.GenericIPAddressField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('ip_address', 'timestamp')
