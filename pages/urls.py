from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('contact', views.contact, name='contact'),
    path('jobs', views.jobs, name='jobs'),
    path('jobs/<int:id>', views.job_detail, name='job_detail'),
    path('search', views.search, name = 'search'),
]