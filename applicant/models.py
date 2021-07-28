from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    CV = models.FileField(null=True, blank=True)
    skill = models.CharField(max_length=255, null=True, blank = True)
    tag_line =  models.CharField(max_length=255, null=True, blank = True)
    introduction =  models.TextField(null=True, blank = True)
    location = models.CharField(max_length=255,null=True, blank = True)
    experience = models.CharField(max_length=255,null=True, blank= True)
    def __str__(self):
        return self.user.username