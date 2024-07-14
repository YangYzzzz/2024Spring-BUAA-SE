"""
推荐文献
"""
from django.db import models
import uuid
from business.models import Paper

from business.utils import storage
from .subclass import Subclass

class recomended_paper(models.Model):
    paper = models.ForeignKey(Paper, on_delete=models.CASCADE)
    recommend_score = models.FloatField(default=0.0, sorted=True)