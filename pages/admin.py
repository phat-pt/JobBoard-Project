from django.contrib import admin
from .models import JobPost, Applicant, ApplicationDetail, Applicant_Profile, Recruiter
from django_summernote.admin import SummernoteModelAdmin

class HeadingAdmin(SummernoteModelAdmin):
    summernote_fields = ('job_description','job_summary')
    list_display = ('ID','job_title','job_location','is_active')
    list_display_links = ('ID', 'job_title')
    search_fields = ('ID','job_title','job_location')
# Register your models here.
# class JobPostAdmin(admin.ModelAdmin):
    

admin.site.register(JobPost, HeadingAdmin)
# admin.site.register(JobPost, JobPostAdmin)
admin.site.register(Applicant)
admin.site.register(ApplicationDetail)
admin.site.register(Applicant_Profile)
admin.site.register(Recruiter)