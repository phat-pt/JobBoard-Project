from django.db import models
from django.contrib.auth.models import User
from django_elasticsearch_dsl import TextField
# Create your models here.

class Applicant_Profile(models.Model):
    ID = models.AutoField(primary_key=True, editable = False),
    exp = models.CharField(max_length=255, null=True, blank = True)
    skill = models.CharField(max_length=255, null=True, blank = True)
    graduate = models.CharField(max_length=255, null=True, blank = True)
    other = models.CharField(max_length=255, null=True, blank = True)
    def __str__(self):
        return self.ID

class Applicant(models.Model):
    ID = models.AutoField(primary_key=True, editable = False)
    a_name = models.CharField(max_length=255, null=True, blank = True)
    a_gender = models.BinaryField(1)
    a_email = models.CharField(max_length=255, null=True, blank= True)
    a_file_upload = models.FileField()
    a_password = models.CharField(max_length=255, null = True, blank= True)
    a_account_status = models.BooleanField(False)
    a_profile =  models.ForeignKey(Applicant_Profile, on_delete=models.SET_NULL,null= True, blank= True)
    def __str__(self):
        return self.a_name

class Recruiter(models.Model):
    ID = models.AutoField(primary_key=True, editable= True)
    r_name = models.CharField(max_length= 255, null= True, blank= True)
    r_email = models.CharField(max_length= 255, null= True, blank= True)
    r_password = models.CharField(max_length= 255, null= True, blank= True)
    r_account_status = models.BooleanField(False)

    def __str__(self):
        return self.r_name

class JobPost(models.Model):
    ID = models.AutoField(primary_key=True, editable = False)
    Recruiter =  models.ForeignKey(Recruiter, on_delete=models.SET_NULL,null= True, blank= True)
    job_title = models.TextField(null=True, blank = True)
    company_name =models.CharField(max_length=255, null=True, blank = True)
    job_location = models.CharField(max_length=255, null=True, blank = True)
    job_description = models.TextField(null=True, blank = True)
    job_summary = models.TextField(null=True, blank = True)
    job_time = models.CharField(max_length=255, null=True, blank = True)
    job_apply_url = models.TextField(null=True, blank = True)
    job_salary = models.CharField(max_length=255, null=True, blank = True)
    job_type = models.CharField(max_length=255, null=True, blank = True)
    company_url = models.TextField(null=True, blank = True)
    is_active = models.BooleanField(True)
    
    def __str__(self):
        return self.job_title


class ApplicationDetail(models.Model):
    ID = models.AutoField(primary_key=True, editable = False)
    applicant_id = models.ForeignKey(Applicant, on_delete=models.SET_NULL,null= True, blank= True)
    job_post_id = models.ForeignKey(JobPost, on_delete= models.SET_NULL,null= True, blank= True)
    application_status = models.BooleanField(False)

    def __str__(self):
        return self.applicant_id

