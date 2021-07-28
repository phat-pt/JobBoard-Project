from django import template
from django.contrib.auth.models import Group 
from employer.models import JobPost
register = template.Library() 
from datetime import datetime

@register.filter(name='has_group') 
def has_group(user, group_name):
    group = Group.objects.filter(name=group_name)
    if group:
        group = group.first()
        return group in user.groups.all()
    else:
        return False

@register.filter(name='is_expired') 
def is_expired(job_post):
    jobpost = JobPost.objects.filter(ID = job_post.ID).get()
    if datetime.today().month - jobpost.job_time.month == 2 and datetime.today().day > jobpost.job_time.day:
        return False
    else:
        return True
