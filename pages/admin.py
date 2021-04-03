from django.contrib import admin
from .models import JobPost, JobType, JobPostSkillSet, SkillSet
# Register your models here.
class JobPostAdmin(admin.ModelAdmin):
    list_display = ('JobTitle','CompanyName', 'CreatedDate','JobLocation','IsActive')
    # list_display_links = ('JobTitle')
    # search_fields = ('JobTitle','CompanyName','JobLocation')

admin.site.register(JobPost, JobPostAdmin)
admin.site.register(JobType)
admin.site.register(JobPostSkillSet)
admin.site.register(SkillSet)