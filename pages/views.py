from django.shortcuts import render, get_object_or_404
from .models import JobPost
from django.core.paginator import EmptyPage, Paginator, PageNotAnInteger
from django_elasticsearch_dsl import Document
from django_elasticsearch_dsl.registries import registry
from .documents import JobPostDocument

# Create your views here.
def home(request):
    jobs = JobPost.objects.all()[:5]
    data = {
        'jobs' : jobs,
    }
    return render(request, 'pages/home.html', data)

def contact(request):
    return render(request, 'pages/contact.html')

def jobs(request):
    jobs = JobPost.objects.all()
    # keyword = request.GET.get('keyword')
    # if keyword:
    #     jobs = JobPostDocument.search().query('match',job_title=keyword)
    # else:
    #     jobs = ''
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
    keyword = request.GET.get('keyword')
    if keyword:
        jobs = JobPostDocument.search().query('match',job_title=keyword)
    else:
        jobs = ''
    data = {
        'jobs' : jobs, 
    }
    return render(request, 'jobs/search.html', data)
