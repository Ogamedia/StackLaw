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


class UserProfile(models.Model):
    """docstring for UserProfile"""
    user = models.OneToOneField(User)
    activation_key = models.Charfield(max_length=40, blank=True)
    key_expires = models.DateTimeField(default-datetime.date.today())
    
    def __unicode__(self):
        return self.user.username
    
    class Meta:
        verbose_name_plural = u'User Profiles'
        