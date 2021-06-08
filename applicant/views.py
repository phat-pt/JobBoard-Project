from typing import ClassVar
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages, auth
from applicant.models import Profile
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from datetime import date
from django.contrib.auth.models import Group

# Create your views here.
def login(request):
    if request.method == 'POST':
        r_username = request.POST['username']
        r_password = request.POST['password']
        user = auth.authenticate(username = r_username, password = r_password)
        if user.groups.filter(name='Applicant').count() == 1:
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
                    user = User.objects.create_user(first_name=r_firstname, last_name= r_lastname, username = r_username, password = r_password, email = r_email )
                    applicant_group = Group.objects.get(name='Applicant') 
                    applicant_group.user_set.add(user)
                    auth.login(request, user)
                    messages.success(request, 'Registered sucessfully')
                    return redirect('home')
        else:
            messages.error(request, "Password do not match")
            return redirect('register')
    else:
        return render(request, 'account/register.html')

def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        return redirect('home')
    return redirect('home')

def profile(request):
    if(User.is_authenticated):
        user = request.user
        profile = Profile.objects.filter(user=request.user).first()
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

            if profile:
                user.first_name = r_firstname
                user.last_name = r_lastname
                user.email = r_email
                profile.skill = r_skill
                profile.tag_line = r_tagline
                profile.introduction  = r_introduction
                if r_CV == "":
                    profile.CV = profile.CV
                else:
                    profile.CV = r_CV
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
                profile = Profile.objects.create(user=user, tag_line=r_tagline, skill = r_skill, CV = r_CV, introduction = r_introduction)
            
    else:
        return redirect('login')
    return render(request, 'account/profile.html', {'profile': profile})
