from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Employer(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE, null=True)
    company_name = models.CharField(max_length=255, null=True, blank = True)
    company_size = models.IntegerField(null=True, blank=True)
    industry = models.CharField(max_length=255, null=True, blank = True)
    address =  models.CharField(max_length=255, null=True, blank = True)
    phone =  models.CharField(max_length=255,null=True, blank = True)
    website = models.CharField(max_length=255,null=True, blank = True)
    introduction = models.TextField(null=True, blank = True)

    def __str__(self):
        return self.user.username

class JobPost(models.Model):
    ID = models.AutoField(primary_key=True, editable = False)
    Employer =  models.ForeignKey(Employer, on_delete=models.CASCADE,null= True, blank= True)
    job_title = models.TextField(null=True, blank = True)
    company_name =models.CharField(max_length=255, null=True, blank = True)
    job_location = models.CharField(max_length=255, null=True, blank = True)
    job_description = models.TextField(null=True, blank = True)
    job_summary = models.TextField(null=True, blank = True)
    job_time = models.DateField(null=True, blank= True)
    job_apply_url = models.TextField(null=True, blank = True)
    job_salary = models.CharField(max_length=255, null=True, blank = True)
    job_type = models.CharField(max_length=255, null=True, blank = True)
    company_url = models.TextField(null=True, blank = True)
    is_active = models.BooleanField(True)
    def __str__(self):
        return self.job_title

class Bookmark(models.Model):
    ID = models.AutoField(primary_key=True, editable = False)
    Employer =  models.ForeignKey(Employer, on_delete=models.CASCADE,null= True, blank= True)
    Applicant =  models.ForeignKey(User, on_delete=models.CASCADE,null= True, blank= True)
    is_active = models.BooleanField(True)
