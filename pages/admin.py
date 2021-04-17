from django.contrib import admin
from .models import JobPost, Applicant, ApplicationDetail, Applicant_Profile, Recruiter
# Register your models here.
class JobPostAdmin(admin.ModelAdmin):
    list_display = ('ID','job_title','job_location','is_active')
    list_display_links = ('ID', 'job_title')
    search_fields = ('ID','job_title','job_location')

admin.site.register(JobPost, JobPostAdmin)
admin.site.register(Applicant)
admin.site.register(ApplicationDetail)
admin.site.register(Applicant_Profile)
admin.site.register(Recruiter)