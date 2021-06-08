from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, request
from django.contrib import messages, auth
from employer.models import JobPost
from applicant.models import Profile
from django.core.paginator import EmptyPage, Paginator, PageNotAnInteger, InvalidPage
from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from elasticsearch_dsl.query import MultiMatch
from .documents import JobPostDocument
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from datetime import date
from django import template
from django.contrib.auth.models import Group 

def home(request):
    jobs = JobPost.objects.all()[:5]

    #AutoComplete
    if "term" in request.GET:
        # qs = JobPost.objects.filter(job_title__istartswith=request.GET.get("term"))
        es_title = JobPostDocument.search().suggest( 'autoc', request.GET.get("term") ,  completion={ 'field': 'job_title', 'skip_duplicates': True }).execute().to_dict()
        es_location = JobPostDocument.search().suggest( 'autoc', request.GET.get("term") ,  completion={ 'field': 'job_location', 'skip_duplicates': True }).execute().to_dict()
        print([suggest['text'] for suggest in es_title['suggest']['autoc'][0]['options']])
        print([suggest['text'] for suggest in es_location['suggest']['autoc'][0]['options']])
        job_titles_locations = [suggest['text'] for suggest in es_title['suggest']['autoc'][0]['options']]+ [suggest['text'] for suggest in es_location['suggest']['autoc'][0]['options']]
        return JsonResponse(job_titles_locations, safe=False)
    data = {
        'jobs' : jobs,
    }
    return render(request, 'pages/home.html', data)



def contact(request):
    return render(request, 'pages/contact.html')

def page_404(request):
    return render(request, 'pages/404.html')

register = template.Library() 

@register.filter(name='has_group') 
def has_group(user, group_name):
    group = Group.objects.filter(name=group_name)
    if group:
        group = group.first()
        return group in user.groups.all()
    else:
        return False

def jobs(request):
    jobs = JobPost.objects.all()
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

def basic_search(keyword, location):
    if keyword and location == "":
        location = "remote"
        query1 = MultiMatch(query=keyword,  fields=['job_description', 'job_title'])
        query2 = MultiMatch(query=location,  fields=['job_location'])
        s = JobPostDocument.search().query(query1 | query2)
    elif location and keyword == "":
        query1 = MultiMatch(query=keyword,  fields=['job_description', 'job_title'])
        query2 = MultiMatch(query=location,  fields=['job_location'])
        s = JobPostDocument.search().query(query2 | query1)
    elif location and keyword:
        query1 = MultiMatch(query=keyword,  fields=['job_description', 'job_title'])
        query2 = MultiMatch(query=location,  fields=['job_location'])
        s = JobPostDocument.search().query(query1 | query2)
    else:
        location = "remote"
        query1 = MultiMatch(query=keyword,  fields=['job_description', 'job_title'])
        query2 = MultiMatch(query=location,  fields=['job_location'])
        s = JobPostDocument.search().query(query2 | query1)

    total = s.count()
    s= s[0:total]
    return s.execute()

def advanced_search(keyword, location, jobtype, min_salary, max_salary):
    if keyword and location == "":
        location = "remote"
        query1 = MultiMatch(query=keyword,  fields=['job_description', 'job_title'])
        query2 = MultiMatch(query=location,  fields=['job_location'])
        query3 = MultiMatch(query=jobtype, fields=['job_type'])
        query4 = MultiMatch(query="$" +min_salary + "$" +max_salary, fields=['job_salary'])
        s = JobPostDocument.search().query(query1 | query2 | query3| query4)
    elif location and keyword == "":
        query2 = MultiMatch(query=location,  fields=['job_location'])
        query3 = MultiMatch(query=jobtype, fields=['job_type'])
        query4 = MultiMatch(query="$" +min_salary + "$" +max_salary, fields=['job_salary'])
        s = JobPostDocument.search().query(query2 | query3| query4)
    elif location and keyword:
        query1 = MultiMatch(query=keyword,  fields=['job_description', 'job_title'])
        query2 = MultiMatch(query=location,  fields=['job_location'])
        query3 = MultiMatch(query=jobtype, fields=['job_type'])
        query4 = MultiMatch(query="$" +min_salary + "$" +max_salary, fields=['job_salary'])
        s = JobPostDocument.search().query(query1 | query2 | query3| query4)
    else:
        location = "remote"
        query2 = MultiMatch(query=location,  fields=['job_location'])
        query3 = MultiMatch(query=jobtype, fields=['job_type'])
        query4 = MultiMatch(query="$" +min_salary + "$" +max_salary, fields=['job_salary'])
        s = JobPostDocument.search().query(query2 | query3| query4)
    total = s.count()
    s= s[0:total]
    return s.execute()

def sorted_advanced_search(keyword, location, jobtype):
    if keyword and location == "":
        location = "remote"
        query1 = MultiMatch(query=keyword,  fields=['job_description', 'job_title'])
        query2 = MultiMatch(query=location,  fields=['job_location'])
        query3 = MultiMatch(query=jobtype, fields=['job_type'])
        s = JobPostDocument.search().query(query1 | query2 | query3).sort({'job_time': "desc"})
    elif location and keyword == "":
        query2 = MultiMatch(query=location,  fields=['job_location'])
        query3 = MultiMatch(query=jobtype, fields=['job_type'])
        s = JobPostDocument.search().query(query2 | query3)
    elif location and keyword:
        query1 = MultiMatch(query=keyword,  fields=['job_description', 'job_title'])
        query2 = MultiMatch(query=location,  fields=['job_location'])
        query3 = MultiMatch(query=jobtype, fields=['job_type'])
        s = JobPostDocument.search().query(query1 | query2 | query3).sort({'job_time': "desc"})
    else:
        location = "remote"
        query2 = MultiMatch(query=location,  fields=['job_location'])
        query3 = MultiMatch(query=jobtype, fields=['job_type'])
        s = JobPostDocument.search().query(query2 | query3).sort({'job_time': "desc"})
    total = s.count()
    s= s[0:total]
    return s.execute()

def jobTypeToText(jobtype):
    if jobtype == "1":
        return "Full-time"
    elif jobtype == "2":
        return "Part-time"
    elif jobtype == "3":
        return "Intership"
    elif jobtype == "4":
        return "Temporary"
    elif jobtype == "5":
        return "Contract"
    else:
        return "Full-time"

def search(request):
    keyword = request.GET.get('keyword',"")
    location = request.GET.get('location',"")
    jobtype = request.GET.get('jobtype', "")
    sort = request.GET.get('sort',"")
    min_salary = request.GET.get('min',"")
    max_salary = request.GET.get('max',"")

    if sort:
        jobs = sorted_advanced_search(keyword, location, jobtype)
    else:
        jobs = advanced_search(keyword, location, jobtype,  min_salary, max_salary)
    paginator = Paginator(jobs, 20)
    page = request.GET.get('page')
    jobs = paginator.get_page(page)
    page_obj = paginator.get_page(jobs)
    return render(request, 'jobs/search.html', {'jobs': jobs, 'page_obj': page_obj})



