from typing import ClassVar
from django.contrib.messages.api import error
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages, auth
from applicant.models import Profile
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from datetime import date
from django.contrib.auth.models import Group

from django.conf import settings
from django.template.loader import render_to_string
from django.views import View

from django.core.mail import send_mail, EmailMessage
from django.urls import reverse
from django.utils.encoding import force_bytes,force_text, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from .utils import token_generator

from django.contrib.auth.decorators import login_required, user_passes_test

# Create your views here.
def login(request):
    if request.method == 'POST':
        r_username = request.POST['username']
        r_password = request.POST['password']
        user = auth.authenticate(username = r_username, password = r_password)
        try:
            if user.groups.filter(name='Applicant'):
                if user is not None:
                    auth.login(request,user)
                    messages.success(request, "Logged in!")
                    return redirect('home')
                else:
                    messages.error(request, "Invallid login credentials!!")
                    return redirect('login')
            else:
                messages.error(request, "Invallid login credentials!!")
                return redirect('login')
        except:
            messages.error(request, "Invallid login credentials!!")
            return redirect('login')
    return render(request, 'account/login.html')

def register(request):
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
                return redirect('register')
            else:
                if User.objects.filter(email=r_email).exists():
                    messages.error(request, 'Email already exists!')
                    return redirect('register')
                else:
                    user = User.objects.create_user(first_name=r_firstname, last_name= r_lastname, username = r_username, password = r_password, email = r_email, is_active = False)
                    applicant_group = Group.objects.get(name='Applicant') 
                    applicant_group.user_set.add(user)

                    uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
                    domain = get_current_site(request).domain
                    link = reverse('activate', kwargs ={
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
                    # auth.login(request, user)

                    messages.success(request, 'Checking your email to activate your account')
                    return redirect('register')
        else:
            messages.error(request, "Password do not match")
            return redirect('register')
    else:
        return render(request, 'account/register.html')

class VerificationView(View):
    def get(self, request, uidb64, token):
        try:
            id = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=id)
            if user.is_active:
                messages.success(request, "User already activated")
                return redirect('login')
            user.is_active= True
            user.save()
            messages.success(request, "User activated successfully")
            return redirect('login')
        except Exception as ex:
            pass
        return redirect('login')


def forgot_password(request):
    r_email = request.POST.get('email',"")
    if r_email:
        user = User.objects.get(email = r_email)
        uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
        domain = get_current_site(request).domain
        link = reverse('resetpassword', kwargs ={
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
        return redirect('forgot_password')

    return render(request, 'account/forgotpassword.html')


class ResetPasswordVerificationView(View):
    def get(self, request, uidb64, token):
        id = force_text(urlsafe_base64_decode(uidb64))
        messages.success(request, "Please create a new password")
        print(id)
        return render(request, 'account/resetpassword.html', {'id': id})

def reset_password(request):
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
            return redirect('login')
        else:
            messages.error(request,"Repeat password do not match")
            return render(request, 'account/resetpassword.html')
    return render(request, 'account/resetpassword.html')

def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        return redirect('home')
    return redirect('home')

@login_required
@user_passes_test(lambda u: u.groups.filter(name='Employer').count() == 0, login_url='/applicant_404')
def profile(request):
    if(User.is_authenticated):
        user = request.user
        profile = Profile.objects.filter(user=request.user).first()
        if profile.CV == None:
            Profile.objects.update(user=user, CV = "None")
        if request.method == 'POST':

            r_firstname = request.POST['firstname']
            r_lastname = request.POST['lastname']
            r_email = request.POST['email']
            r_skill = request.POST['skill']
            r_tagline = request.POST['tagline']
            r_introduction = request.POST['introduction']
            r_current_password = request.POST['current_password']
            r_new_password = request.POST['new_password']   
            r_repeat_password = request.POST['repeat_password'] 
            r_CV = request.FILES.get('CV',"")
            r_location = request.POST['location']
            r_experience = request.POST['experience']
            r_experience_time = request.POST['experience_time']

            if profile:
                user.first_name = r_firstname
                user.last_name = r_lastname
                user.email = r_email
                profile.skill = r_skill
                profile.tag_line = r_tagline
                profile.introduction  = r_introduction
                profile.CV = r_CV
                profile.location = r_location
                profile.experience = r_experience +" "+ r_experience_time
                user.save()
                profile.save()
                messages.success(request, "Updated Successfully")
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
                            return redirect('profile')
            else:
                profile = Profile.objects.create(user=user, tag_line=r_tagline, skill = r_skill, CV = r_CV, introduction = r_introduction, experience = r_experience +" "+ r_experience_time)
    else:
        return redirect('login')
    if profile.experience:
        experiencetime = profile.experience.split(" ")[1]
        profile.experience = profile.experience.split(" ")[0]
    return render(request, 'account/profile.html', {'profile': profile, 'experiencetime' : experiencetime})

def delete_CV(request):
    profile = Profile.objects.filter(user=request.user).first()
    try:
        profile.CV.delete()
        return redirect('profile')
    except:
        messages.error(request,"Can not delete!!")
        return redirect('profile')
