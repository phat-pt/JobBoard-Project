from django.urls import path, include
from . import views
import employer

urlpatterns = [
    #Account
    path('employer_login', views.employer_login, name = 'employer_login'),
    path('employer_register', views.employer_register, name = 'employer_register'),
    path('employer_logout', views.employer_logout, name = 'employer_logout'),
    path('employer_profile', views.employer_profile, name='employer_profile'),
    path('employer_company_register', views.employer_company_register, name ='employer_company_register'),

    path('dashboard', views.dashboard, name = 'dashboard'),
    path('jobs', views.job_list, name = 'job_list'),
    path('postjob', views.post_job, name = 'post_job'),
    path('jobs/<int:id>', views.edit_job, name='edit_job'),
    path('search', views.search_job, name = 'search_job'),
    path('delete/<int:id>', views.delete_job, name = 'delete_job'),
    path('applicants', views.applicant_list, name='applicant_list'),
    path('applicant_search', views.applicant_search, name='applicant_search'),
    path('applicant_detail/<int:id>', views.applicant_detail, name='applicant_detail'),
]