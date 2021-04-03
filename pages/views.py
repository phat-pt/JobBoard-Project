from django.shortcuts import render
from .models import JobPost

# Create your views here.
def home(request):
    jobs = JobPost.objects.all()
    data = {
        'jobs' : jobs,
    }
    return render(request, 'pages/home.html', data)

def contact(request):
    return render(request, 'pages/contact.html')

def jobs(request):
    return render(request, 'pages/jobs.html')