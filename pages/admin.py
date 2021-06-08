from django.contrib import admin
from .models import *
from applicant.models import *
from employer.models import *
from django_summernote.admin import SummernoteModelAdmin

class HeadingAdmin(SummernoteModelAdmin):
    summernote_fields = ('job_description','job_summary')
    list_display = ('ID','job_title','job_location','is_active')
    list_display_links = ('ID', 'job_title')
    search_fields = ('ID','job_title','job_location')

class HeadingProfile(SummernoteModelAdmin):
    summernote_fields = ('introduction')
# Register your models here.
# class JobPostAdmin(admin.ModelAdmin):

class HeadingEmployer(SummernoteModelAdmin):
    summernote_fields = ('introduction')
    

admin.site.register(JobPost, HeadingAdmin)
# # admin.site.register(JobPost, JobPostAdmin)
# admin.site.register(Applicant)
# admin.site.register(ApplicationDetail)
admin.site.register(Profile)
admin.site.register(Employer,HeadingEmployer)