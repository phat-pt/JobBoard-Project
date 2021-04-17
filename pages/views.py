from django.shortcuts import render, get_object_or_404
from .models import JobPost
from django.core.paginator import EmptyPage, Paginator, PageNotAnInteger

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
    jobs = JobPost.objects.all()
    
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
    if 'location' in request.GET:
        location = request.GET['location']
        if keyword:
            jobs = jobs.filter(job_description__icontains = keyword).filter(job_location__icontains = location)

    paginator = Paginator(jobs, 50) 
    page = request.GET.get('page')
    paged_jobs = paginator.get_page(page)
    data = {
        'jobs' : paged_jobs,
    }
    return render(request, 'jobs/jobs.html', data)

def job_detail(request, id):
    single_job = get_object_or_404(JobPost, pk= id)
    data = {
        'single_job' : single_job,
    }
    return render(request, 'pages/job_detail.html', data)

def search(request):
    jobs = JobPost.objects.all()
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
    if 'location' in request.GET:
        location = request.GET['location']
        if location or location:
            jobs = jobs.filter(job_location__icontains = location)
    data = {
        'jobs' : jobs, 
    }
    return render(request, 'jobs/search.html', data)