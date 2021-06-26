from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('404', views.page_404_employer, name ='page_404'),
    path('applicant_404', views.page_404_applicant, name ='page_404_applicant'),
    #JobPosts
    path('jobs', views.jobs, name='jobs'),
    path('jobs/<int:id>', views.job_detail, name='job_detail'),
    path('search', views.search, name = 'search'),
    path('sort', views.search, name = 'sort'),
    path('company_detail/<int:id>', views.company_detail, name = 'company_detail'),
    path('apply_job/<int:id>', views.apply_job, name = 'apply_job'),
    path('send_apply_job/<int:id>', views.send_apply_job, name = 'send_apply_job'),
]