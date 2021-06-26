from django.contrib.admin.options import TabularInline
from pages.views import search
import employer
from typing import ClassVar
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages, auth
from employer.models import Bookmark, Employer
from django.contrib.auth.models import User
from employer.models import JobPost
from applicant.models import Profile
from django.contrib.auth import authenticate, login
from datetime import date, datetime
from django.core.paginator import EmptyPage, Paginator, PageNotAnInteger, InvalidPage
from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from elasticsearch_dsl.query import MultiMatch
from pages.documents import JobPostDocument
from .documents import ProfileDocument
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse
import json
from django.utils import timezone

from django.core.mail import send_mail, EmailMessage
from django.urls import reverse
from django.utils.encoding import force_bytes,force_text, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from .utils import token_generator
from django.views import View

# Create your views here.
@login_required
@user_passes_test(lambda u: u.groups.filter(name='Applicant').count() == 0, login_url='/404')
def dashboard(request):
    if Employer.objects.filter(user=request.user).exists():
        employer = Employer.objects.filter(user=request.user).first()
        bookmarks = Bookmark.objects.filter(Employer = request.user.employer.id, is_active=True)
        jobs = JobPost.objects.filter(Employer = employer).order_by('-job_time').all()[:5]
        job_count = JobPost.objects.filter(Employer = employer).all().count()
        applicant_count = User.objects.filter(groups__name='Applicant').all().count()
        applicant_join_today = User.objects.filter(groups__name='Applicant').filter(date_joined__day=datetime.today().day).all().count()
        return render(request, 'employer/dashboard.html', {"bookmarks" : bookmarks, "jobs":jobs, "applicant_count": applicant_count, "job_count" : job_count ,
        "applicant_join_today": applicant_join_today})
    else:
        return redirect('employer_company_register')


@login_required
@user_passes_test(lambda u: u.groups.filter(name='Applicant').count() == 0, login_url='/404')
def job_list(request):
    employer = Employer.objects.filter(user=request.user).first()
    jobs = JobPost.objects.filter(Employer = employer).order_by('-job_time').all()
 
    paginator = Paginator(jobs, 5)
    page = request.GET.get('page')
    jobs = paginator.get_page(page)

    data = {
        'jobs' : jobs,
    }
    return render(request, 'employer/jobs.html', data)

@login_required
@user_passes_test(lambda u: u.groups.filter(name='Applicant').count() == 0, login_url='/404')
def search_job(request):
    employer = Employer.objects.filter(user=request.user).first()
    keyword = request.GET.get('keyword',"")
    jobs = JobPost.objects.filter(Employer = employer).filter(job_title__icontains=keyword).order_by('-job_time')
    paginator = Paginator(jobs, 5)
    page = request.GET.get('page')
    jobs = paginator.get_page(page)
    return render(request, 'employer/jobs.html', {'jobs': jobs})

@login_required
@user_passes_test(lambda u: u.groups.filter(name='Applicant').count() == 0, login_url='/404')
def post_job(request):
    employer = Employer.objects.filter(user=request.user).first()
    if employer:

        if request.method == 'POST':
            r_job_title = request.POST.get('job_title',"")
            r_job_location = request.POST.get('job_location',"")
            r_job_type = request.POST.get('job_type',"")
            r_job_salary = request.POST.get('job_salary',"")
            r_job_apply_url = request.POST.get('job_apply_url',"")
            r_job_summary = request.POST.get('job_summary',"")
            r_job_description = request.POST.get('job_description',"")

            if employer.company_name and employer.website:
                jobpost = JobPost(Employer = employer,job_title= r_job_title, company_name  =  employer.company_name , job_location = r_job_location, job_description = r_job_description,
                job_summary =r_job_summary, job_time= date.today(), job_apply_url = r_job_apply_url, job_salary = r_job_salary, job_type = r_job_type,
                company_url = employer.website, is_active = True)
                jobpost.save()
                messages.success(request, "Create successfully!")
                return redirect('job_list')
            else:
                messages.error(request, "You must finish your company profile")
                return redirect('employer_profile')
    else:
        messages.error(request, "You must finish your company profile")
        return redirect('employer_profile')
    return render(request, 'employer/postjob.html')

@login_required
@user_passes_test(lambda u: u.groups.filter(name='Applicant').count() == 0, login_url='/404')
def edit_job(request, id):
    employer = Employer.objects.filter(user=request.user).first()
    job = get_object_or_404(JobPost, pk= id)
    data = {
        'job' : job,
    }
    if request.method == 'POST':
        r_job_title = request.POST.get('job_title',"")
        r_job_location = request.POST.get('job_location',"")
        r_job_type = request.POST.get('job_type',"")
        r_job_salary = request.POST.get('job_salary',"")
        r_job_apply_url = request.POST.get('job_apply_url',"")
        r_job_summary = request.POST.get('job_summary',"")
        r_job_description = request.POST.get('job_description',"")
        
        job = JobPost.objects.filter(pk=id).update(Employer = employer,job_title= r_job_title, company_name  =  employer.company_name, job_location = r_job_location, job_description = r_job_description,
        job_summary =r_job_summary, job_time= date.today(), job_apply_url = r_job_apply_url, job_salary = r_job_salary, job_type = r_job_type,
        company_url = employer.website, is_active = True)
        messages.success(request, "Update successfully!")
        return redirect('job_list')
        
    return render(request, 'employer/editjob.html', data)

@login_required
@user_passes_test(lambda u: u.groups.filter(name='Applicant').count() == 0, login_url='/404')
def delete_job(request, id):
    job = get_object_or_404(JobPost, pk= id)
    try:
        job.delete()
        messages.success(request,"Deleted!!")
        return redirect('job_list')
    except:
        messages.error(request,"Can not delete!!")
        return redirect('job_list')

def employer_login(request):
    if request.method == 'POST':
        r_username = request.POST['username']
        r_password = request.POST['password']
        user = auth.authenticate(username = r_username, password = r_password)
        
        try:
            if user.groups.filter(name='Employer'):
                if user is not None:
                    auth.login(request,user)
                    if Employer.objects.filter(user=request.user).exists():
                        return redirect('dashboard')
                    else:
                        messages.success(request, "Please fill out this form to complete your company information!")
                        return redirect('employer_company_register')
                else:
                    messages.error(request, "Invallid login credentials!!")
                    return redirect('employer_login')
            else:
                messages.error(request, "Invallid login credentials!!")
                return redirect('employer_login')
        except:
            messages.error(request, "Invallid login credentials!!")
            return redirect('employer_login')
    return render(request, 'employer/login.html')

def employer_register(request):
    if request.method == 'POST':
        r_username = request.POST['username']
        r_firstname = request.POST['firstname']
        r_lastname = request.POST['lastname']
        r_email = request.POST['email']
        r_password = request.POST['password']
        r_repeat_password = request.POST['repeat_password'] 

        if r_password == r_repeat_password:
            if User.objects.filter(username=r_username).exists():
                messages.error(request, 'Username already exists!')
                return redirect('employer_register')
            else:
                if User.objects.filter(email=r_email).exists():
                    messages.error(request, 'Email already exists!')
                    return redirect('employer_register')
                else:
                    user = User.objects.create_user(first_name=r_firstname, last_name= r_lastname, username = r_username, password = r_password, email = r_email, is_active=False)
                    applicant_group = Group.objects.get(name='Employer') 
                    applicant_group.user_set.add(user)


                    uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
                    domain = get_current_site(request).domain
                    link = reverse('employer_activate', kwargs ={
                        'uidb64' : uidb64, 'token' : token_generator.make_token(user)
                    })
                    activate_url = domain[:-1] + link 
                    email_subject = "Activate your account for JobSearch"
                    email_body ='Hi ' + user.username + '. Please use this link to verify your account\n' + activate_url

                    email = EmailMessage(
                        email_subject,
                        email_body,
                        'norely@semicolon.com',
                        [r_email],
                    )
                    email.send(fail_silently=False)

                    messages.success(request, "Check your mail to activate your account")
                    # auth.login(request, user)
                    return redirect('employer_register')
        else:
            messages.error(request, "Password do not match")
            return redirect('employer_register')
    else:
        return render(request, 'employer/register.html')


class VerificationView(View):
    def get(self, request, uidb64, token):
        try:
            id = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=id)
            if user.is_active:
                messages.success(request, "User already activated")
                return redirect('employer_login')
            user.is_active= True
            user.save()
            messages.success(request, "User activated successfully")
            return redirect('employer_login')
        except Exception as ex:
            pass
        return redirect('employer_login')

def employer_forgot_password(request):
    r_email = request.POST.get('email',"")
    if r_email:
        user = User.objects.get(email = r_email)
        uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
        domain = get_current_site(request).domain
        link = reverse('employer_resetpassword', kwargs ={
            'uidb64' : uidb64, 'token' : token_generator.make_token(user)
        })
        activate_url = domain[:-1] + link 
        email_subject = "Reset your password JobSearch"
        email_body ='Hi ' + user.username + '. Please use this link to reset your password\n' + activate_url

        email = EmailMessage(
            email_subject,
            email_body,
            'norely@semicolon.com',
            [r_email],
        )
        email.send(fail_silently=False)
        messages.success(request, "Check your mail to reset password")
        return redirect('employer_forgot_password')
    return render(request, 'employer/forgotpassword.html')


class ResetPasswordVerificationView(View):
    def get(self, request, uidb64, token):
        id = force_text(urlsafe_base64_decode(uidb64))
        messages.success(request, "Please create a new password")
        return render(request, 'employer/resetpassword.html', {'id': id})

def employer_reset_password(request):
    r_new_password = request.POST.get('new_password',"")
    r_repeat_password = request.POST.get('repeat_password',"")
    r_id = request.POST.get("id")
    user = User.objects.get(pk = r_id)
    print(r_new_password,r_repeat_password, r_id, user)
    if r_new_password != "" and r_repeat_password != "":
        if r_new_password == r_repeat_password:
            user.set_password(r_new_password)
            user.save()
            messages.success(request,"Change password complete, please login")
            return redirect('employer_login')
        else:
            messages.error(request,"Repeat password do not match")
            return render(request, 'employer/resetpassword.html')
    return render(request, 'employer/resetpassword.html')



@login_required
@user_passes_test(lambda u: u.groups.filter(name='Applicant').count() == 0, login_url='/404')
def employer_company_register(request):
    if(User.is_authenticated):
        user = request.user
        employer = Employer.objects.filter(user=request.user).first()
    if request.method == 'POST':
        r_company_name = request.POST.get('companyname',"")
        r_company_size = request.POST.get("companysize","0")
        r_industry = request.POST.get('industry',"")
        r_address = request.POST.get("address","")
        r_phone = request.POST.get("phone","")
        r_website = request.POST.get("website","")
        r_introduction = request.POST.get("introduction","")

        Employer.objects.create(user=user, company_name = r_company_name, company_size = r_company_size, industry = r_industry, 
                address= r_address, phone = r_phone, website = r_website, introduction  = r_introduction)

       
        return redirect('dashboard')
    else:
        return render(request, 'employer/registerprofile.html')

def employer_logout(request):
    if request.method == 'POST':
        auth.logout(request)
        return redirect('dashboard')
    return redirect('dashboard')

@login_required
@user_passes_test(lambda u: u.groups.filter(name='Applicant').count() == 0, login_url='/404')
def employer_profile(request):
    if(User.is_authenticated):
        user = request.user
        employer = Employer.objects.filter(user=request.user).first()
        
        if request.method == 'POST':
            r_firstname = request.POST['firstname']
            r_lastname = request.POST['lastname']
            r_email = request.POST['email']
            r_current_password = request.POST['current_password']
            r_new_password = request.POST['new_password']   
            r_repeat_password = request.POST['repeat_password'] 


            r_company_name = request.POST.get('companyname',"")
            r_company_size = request.POST.get("companysize","0")
            r_industry = request.POST.get('industry',"")
            r_address = request.POST.get("address","")
            r_phone = request.POST.get("phone","")
            r_website = request.POST.get("website","")
            r_introduction = request.POST.get("introduction","")

            print(r_company_name)
            if employer:
                user.first_name = r_firstname
                user.last_name = r_lastname
                user.email = r_email

                Employer.objects.filter(id = employer.id).update(user=user, company_name = r_company_name, company_size = r_company_size, industry = r_industry, 
                address= r_address, phone = r_phone, website = r_website, introduction  = r_introduction)
                user.save()
                if r_current_password:
                    user = auth.authenticate(username = user.username, password = r_current_password)
                    if user is not None:
                        if(r_new_password == r_repeat_password):
                            user.set_password(r_new_password)
                            user.save()
                            messages.success(request, "Please Login Again")
                            return redirect('login')
                        else:
                            messages.error(request, "Repeat Password do not match!!!")
                            return redirect('employer_profile')
            else:
                employer = Employer.objects.create(user=user, company_name = r_company_name, company_size = r_company_size, industry = r_industry, 
                address= r_address, phone = r_phone, website = r_website, introduction  = r_introduction)
    else:
        return redirect('login')
    return render(request, 'employer/employerprofile.html', {'employer': employer})


@login_required
@user_passes_test(lambda u: u.groups.filter(name='Applicant').count() == 0, login_url='/404')
def applicant_list(request):
    applicants = User.objects.filter(groups__name='Applicant').all()
    print(applicants)
    paginator = Paginator(applicants, 5)
    page = request.GET.get('page')
    applicants = paginator.get_page(page)
    return render(request, 'employer/applicants.html', {'applicants': applicants})

@login_required
@user_passes_test(lambda u: u.groups.filter(name='Applicant').count() == 0, login_url='/404')
def applicant_search(request):
    r_keyword = request.GET.get('keyword',"")
    r_location = request.GET.get('location',"")
    r_skill = request.GET.get('skill', "")
    if r_keyword or r_location or r_skill:
        query1 = MultiMatch(query=r_keyword,  fields=['tag_line'])
        query2 = MultiMatch(query=r_location,  fields=['location'])
        query3 = MultiMatch(query=r_skill, fields=['skill'])
        s = ProfileDocument.search().query(query1 | query2 | query3)
        total = s.count()
        s= s[0:total]
        profiles =  s.execute()
        profile_id = [profile.id for profile in profiles]
        print(profile_id)
        applicants = User.objects.filter(profile__in = profile_id)
    else:
        applicants = User.objects.filter(groups__name='Applicant').all()
    paginator = Paginator(applicants, 5)
    page = request.GET.get('page')
    applicants = paginator.get_page(page)
    return render(request, 'employer/applicants.html', {'applicants': applicants})

@login_required
@user_passes_test(lambda u: u.groups.filter(name='Applicant').count() == 0, login_url='/404')
def applicant_detail(request, id):
    r_bookmark = request.POST.get('bookmark',"")
    applicant = get_object_or_404(User, pk= id)
    profile = Profile.objects.filter(user=applicant).get()
    if Bookmark.objects.filter(Applicant = id, Employer = request.user.employer.id).exists():
        bookmark = Bookmark.objects.filter(Applicant = id, Employer = request.user.employer.id).get()
    else:
        bookmark = Bookmark.objects.create(Applicant = applicant, Employer = request.user.employer, is_active = False)
    skills = profile.skill.strip().split(",")
    if r_bookmark == "True":
        bookmark.is_active = False
        bookmark.save()
    elif r_bookmark == "False":
        bookmark.is_active = True
        bookmark.save()
    else:
        bookmark = Bookmark.objects.filter(Applicant = id, Employer = request.user.employer.id).get()
    return render(request, 'employer/applicantdetail.html', {'applicant': applicant, 'skills' : skills,'bookmark': bookmark})
