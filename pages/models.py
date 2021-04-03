from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class JobType(models.Model):
    JobType = models.CharField(max_length=200, null=True, blank = True)
    ID = models.AutoField(primary_key=True, editable = False)
    def __str__(self):
        return self.JobType

class SkillSet(models.Model):
    SkillSetName = models.CharField(max_length=200, null=True, blank = True)
    ID = models.AutoField(primary_key=True, editable = False)
    def __str__(self):
        return self.SkillSetName

class JobPost(models.Model):
    JobTypeID = models.ForeignKey(JobType, on_delete=models.SET_NULL, null = True)
    CompanyName = models.CharField(max_length=200, null=True, blank = True)
    CreatedDate = models.DateTimeField(auto_now_add = True)
    JobTitle = models.CharField(max_length=200, null=True, blank = True)
    JobDescription = models.TextField(null=True, blank = True)
    JobLocation = models.CharField(max_length=200, null=True, blank = True)
    IsActive = models.BooleanField(True)
    ID = models.AutoField(primary_key=True, editable = False)
    def __str__(self):
        return self.JobTitle

class JobPostSkillSet(models.Model):
    SkillLevel = models.DecimalField(max_digits=5, decimal_places=2, null = True, blank = True)
    JobPostID = models.ForeignKey(JobPost, on_delete=models.SET_NULL, null = True)
    SkillSetID = models.ForeignKey(SkillSet, on_delete=models.SET_NULL, null = True)
    def __str__(self):
        return self.SkillLevel
