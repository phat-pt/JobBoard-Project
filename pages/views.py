from django.shortcuts import render, get_object_or_404
from .models import JobPost
from django.core.paginator import EmptyPage, Paginator, PageNotAnInteger
from django_elasticsearch_dsl import Document
from django_elasticsearch_dsl.registries import registry
from elasticsearch_dsl.query import MultiMatch
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
    paginator = Paginator(jobs, 10) 
    page = request.GET.get('page')
    
    try:
        paged_jobs = paginator.page(page)
    except PageNotAnInteger:
        paged_jobs = paginator.page(1)
    except EmptyPage:
        paged_jobs = paginator.page(paginator.num_pages)
    data = {
        'jobs' : paged_jobs,
    }
    return render(request, 'jobs/search.html', data)

def job_detail(request, id):
    single_job = get_object_or_404(JobPost, pk= id)
    data = {
        'single_job' : single_job,
    }
    return render(request, 'pages/job_detail.html', data)


def search(request):
    keyword = request.GET.get('keyword')
    location = request.GET.get('location')
    if keyword and location == "":
        keyword = request.GET.get('keyword', "")
        location = "remote"
        query1 = MultiMatch(query=keyword,  fields=['job_description', 'job_title'])
        query2 = MultiMatch(query=location,  fields=['job_location'])
        s = JobPostDocument.search().query(query1 | query2)
        total = s.count()
        s= s[0:total]
        jobs = s.execute()

        paginator = Paginator(jobs, 20)
        page = request.GET.get('page')
        jobs = paginator.get_page(page)

    elif location and keyword == "":
        keyword = request.GET.get('keyword', "")
        location = request.GET.get('location', "")
        query1 = MultiMatch(query=keyword,  fields=['job_description', 'job_title'])
        query2 = MultiMatch(query=location,  fields=['job_location'])
        s = JobPostDocument.search().query(query2 | query1)
        total = s.count()
        s= s[0:total]
        jobs = s.execute()

        paginator = Paginator(jobs, 20)
        page = request.GET.get('page')
        jobs = paginator.get_page(page)

    elif location and keyword:
        keyword = request.GET.get('keyword', "")
        location = request.GET.get('location', "")
        query1 = MultiMatch(query=keyword,  fields=['job_description', 'job_title'])
        query2 = MultiMatch(query=location,  fields=['job_location'])
        s = JobPostDocument.search().query(query1 | query2)
        total = s.count()
        s= s[0:total]
        jobs = s.execute()

        paginator = Paginator(jobs, 20)
        page = request.GET.get('page')
        jobs = paginator.get_page(page)
    
    else:
        keyword = request.GET.get('keyword', "")
        location = "remote"
        query1 = MultiMatch(query=keyword,  fields=['job_description', 'job_title'])
        query2 = MultiMatch(query=location,  fields=['job_location'])
        s = JobPostDocument.search().query(query2 | query1)
        total = s.count()
        s= s[0:total]
        jobs = s.execute()

        paginator = Paginator(jobs, 20)
        page = request.GET.get('page')
        jobs = paginator.get_page(page)

    return render(request, 'jobs/search.html', {'jobs': jobs})


