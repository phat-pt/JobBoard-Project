from os import pipe
from typing import Match
from django.db.models.query import RawQuerySet
from django.http.response import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, request
from django.contrib import messages, auth
from employer.models import Employer, JobPost
from applicant.models import Profile
from django.core.paginator import EmptyPage, Paginator, PageNotAnInteger, InvalidPage
from django_elasticsearch_dsl.registries import registry
from elasticsearch_dsl.query import MultiMatch
from .documents import JobPostDocument
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from datetime import date
from django import template
from django.contrib.auth.models import Group 
from django.core.mail import send_mail, EmailMessage
from django.contrib.auth.decorators import login_required, user_passes_test
from datetime import date, datetime

def home(request):
    user = request.user
    if (user.is_authenticated):
        if user.groups.filter(name='Applicant').exists() == False and user.groups.filter(name='Employer').exists() == False:
            applicant_group = Group.objects.get(name='Applicant') 
            applicant_group.user_set.add(user)
            user.is_staff = False   
            user.save()
    jobs = JobPost.objects.order_by('-job_time').all()[:5]
    #AutoComplete
    if "term" in request.GET:
        # qs = JobPost.objects.filter(job_title__istartswith=request.GET.get("term"))
        es_title = JobPostDocument.search().suggest( 'autoc', request.GET.get("term") ,  completion={ 'field': 'job_title.suggest', 'skip_duplicates': True }).execute().to_dict()
        es_location = JobPost.objects.filter(job_location__icontains = request.GET.get("term")).all()[:5]
        #es_title = JobPost.objects.filter(job_title__icontains = request.GET.get("term")).all()[:5]
        job_titles_locations = [suggest['text'] for suggest in es_title['suggest']['autoc'][0]['options']] + [job.job_location for job in es_location]
        # job_titles_locations = [job.job_title for job in es_location] + [job.job_location for job in es_location]
        return JsonResponse(job_titles_locations, safe=False)
    if (user.is_authenticated):
        profile = Profile.objects.filter(user=request.user).first()
        if profile:
            if profile.skill == None or profile.skill == "":
                jobs = JobPost.objects.order_by('-job_time').all()[:5]
            else:
                s = JobPostDocument.search().query(MultiMatch(query = profile.skill ,fields=['job_description', 'job_title']))
                s = s[0:5]
                jobs = s.execute()
        else:
            Profile.objects.create(user=user)
    data = {
        'jobs' : jobs,
    }
    return render(request, 'pages/home.html', data)

def page_404_employer(request):
    messages.error(request,"Please login as Employer!!")
    return render(request, 'pages/404.html')

def page_404_applicant(request):
    messages.error(request,"Please login as Applicant!!")
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
    return render(request, 'pages/search.html', data)

def job_detail(request, id):
    single_job = get_object_or_404(JobPost, pk= id)
    es_title = JobPostDocument.search().suggest( 'autoc', single_job.job_title ,  completion={ 'field': 'job_title.suggest', 'skip_duplicates': True }).execute().to_dict()
    suggested_jobs = [suggest['_source'] for suggest in es_title['suggest']['autoc'][0]['options']]
    return render(request, 'pages/job_detail.html', {'single_job' : single_job, 'suggested_job' : suggested_jobs[0:4]})

def advanced_search(keyword, location, jobtype, min_salary, max_salary,salary_type, sort ):
    query1 = MultiMatch(query=keyword,  fields=['job_title','job_description'])
    query2 = MultiMatch(query=location,  fields=['job_location'])
    query3 = MultiMatch(query=jobtype, fields=['job_type'])
    query4 = MultiMatch(query="$" +min_salary + "$" +max_salary + salary_type, fields=['job_salary'])

    if keyword and location and jobtype and min_salary and max_salary:
        s = JobPostDocument.search().query(query1 & query2 & query3 & query4)
    elif keyword and location and jobtype:
        s = JobPostDocument.search().query(query1 & query2 & query3)
    elif keyword and location and min_salary and max_salary:
        print("hear")
        s = JobPostDocument.search().query(query1 & query2 & query4)
    elif keyword and jobtype and min_salary and max_salary:
        s = JobPostDocument.search().query(query1 & query3 & query4)
    elif keyword and location:
        s = JobPostDocument.search().query(query1 & query2)
    elif keyword and jobtype:
        s = JobPostDocument.search().query(query1 & query3)
    elif keyword and min_salary and max_salary:
        s = JobPostDocument.search().query(query1 & query4)
    elif keyword:
        s = JobPostDocument.search().query(query1)
    elif location:
        s = JobPostDocument.search().query(query2)
    elif min_salary: 
        s = JobPostDocument.search().query(MultiMatch(query=min_salary, fields=['job_salary']))
    elif max_salary: 
        s = JobPostDocument.search().query(MultiMatch(query=max_salary, fields=['job_salary']))
    elif jobtype:
        s = JobPostDocument.search().query(query3) 
    else:
        location = "remote"
        query2 = MultiMatch(query=location,  fields=['job_location'])
        s = JobPostDocument.search().query(query2).sort({'job_time': "desc"})
    if sort:
        s = s.sort({'job_time': "desc"})
    total = s.count()
    s= s[0:total]
    return s.execute(), total


def search(request):
    keyword = request.GET.get('keyword',"")
    location = request.GET.get('location',"")
    jobtype = request.GET.get('jobtype', "")
    sort = request.GET.get('sort',"")
    min_salary = request.GET.get('min',"")
    max_salary = request.GET.get('max',"")
    salary_type = request.GET.get('salarytype',"")

    jobs, total = advanced_search(keyword, location, jobtype, min_salary, max_salary,salary_type, sort)
    paginator = Paginator(jobs, 20)
    page = request.GET.get('page')
    jobs = paginator.get_page(page)
    page_obj = paginator.get_page(jobs)
    return render(request, 'pages/search.html', {'jobs': jobs, 'page_obj': page_obj, 'total' : total})

def company_detail(request, id):
    company = get_object_or_404(Employer, pk = id)
    jobs = JobPost.objects.filter(Employer = company.pk).order_by("-job_time").all()[:5]
    return render(request, 'pages/company.html', {'company': company, 'jobs': jobs})

def apply_job(request, id):
    if(request.user.is_authenticated):
        single_job = get_object_or_404(JobPost, pk= id)
        data = {
            'single_job' : single_job,
        }
        return render(request, 'pages/applyjob.html', data)
    else:
        return redirect('login')

def send_apply_job(request, id):
    single_job = get_object_or_404(JobPost, pk= id)
    employer = Employer.objects.filter(pk = single_job.Employer.id).get()
    user = User.objects.filter(employer = employer).get()
    if request.method == 'POST':
        r_name = request.POST.get("name","")
        r_email = request.POST.get("email","")
        r_CV = request.FILES.get('CV',"")
        r_cover_letter = request.POST.get("coverletter","")
        print(r_cover_letter, user.email, r_CV)
        if r_CV and r_cover_letter:
            email_subject = "[JobSearch] " + r_name + " had applied to your " + single_job.job_title + " job."
            email_body = "Cover Letter: \n" + r_cover_letter +  "\nEmail Adress: \n" + r_email
            email = EmailMessage(
                email_subject,
                email_body,
                'norely@semicolon.com',
                [user.email],
            )
            print(user.email)
            email.attach(r_CV.name, r_CV.read(), r_CV.content_type)
            email.send(fail_silently=False)
            messages.success(request, "Apply job successful")
    return redirect('apply_job', id)


