from django.db import models
import datetime
from django.utils import timezone

# Create your models here.
class ReviewRequest(models.Model):
    """docstring for ClassName"""
    description = models.TextField(max_length=400)
    body = models.TextField()
    
    def __unicode__(self):
        return self.title
        