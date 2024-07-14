"""
数据库文献表
"""
from django.db import models
import uuid

from business.utils import storage
from .subclass import Subclass


class Paper(models.Model):
    """
    Field:
        - paper_id         文献ID
        - title            文献标题
        - authors          作者
        - abstract         摘要
        - publication_date 发布时间
        - journal          期刊
        - citation_count   引用次数
        - original_url     原文地址
        - read_count       阅读次数
        - like_count       点赞次数
        - collect_count    收藏次数
        - comment_count    评论次数
        - download_count   下载次数
        - score            评分
        - score_count      评分次数
        - local_path       本地地址
    """
    paper_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    title = models.CharField(max_length=255)
    authors = models.CharField(max_length=255)  # 多个作者','分隔
    abstract = models.TextField()
    publication_date = models.DateField()
    journal = models.CharField(max_length=255, null=True)  # 期刊允许为空
    citation_count = models.IntegerField(default=0)
    original_url = models.URLField()
    read_count = models.IntegerField(default=0)
    like_count = models.IntegerField(default=0)
    collect_count = models.IntegerField(default=0)
    comment_count = models.IntegerField(default=0)
    download_count = models.IntegerField(default=0)
    score = models.FloatField(default=0.0)
    score_count = models.IntegerField(default=0)
    local_path = models.CharField(max_length=255)  # 本地地址，允许为空
    sub_classes = models.ManyToManyField(Subclass, related_name='papers')

    def __str__(self):
        return self.title

    def simply_desc(self):
        return {
            'paper_id': str(self.paper_id),
            'title': str(self.title),
        }

    def get_paper_id(self):
        return str(self.paper_id)

    def to_dict(self):
        return {
            'paper_id': self.paper_id,
            'title': self.title,
            'authors': self.authors,
            'abstract': self.abstract,
            'publication_date': self.publication_date,
            'journal': self.journal,
            'citation_count': self.citation_count,
            'original_url': self.original_url,
            'read_count': self.read_count,
            'like_count': self.like_count,
            'collect_count': self.collect_count,
            'comment_count': self.comment_count,
            'download_count': self.download_count,
            'score': self.score,
            'score_count': self.score_count,
            'sub_classes': list(self.sub_classes.values_list('name', flat=True))
        }

    def __eq__(self, other):
        return self.paper_id == other.paper_id if isinstance(other, Paper) else False

    def __hash__(self):
        return hash(self.paper_id)
