from django.contrib.auth import  login, logout,authenticate
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.conf import settings
from accounts.forms import SignupForm,AccountAuthenticateForm
from accounts.models import DogAccount

import pandas as pd
import csv
# Create your views here.
#creating a signup view page



def register_view(request,*args,**kwargs):
    user = request.user
    if user.is_authenticated:
        return HttpResponse(f'you are already autheticated as {user.email}')
    context = {}
    if request.POST:
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email').lower()
            raw_password = form.cleaned_data.get('password1')
            dog_account = authenticate(email=email,password = raw_password)
            login(request,dog_account)
            destination = get_redirect_if_exist(request)
            if destination:
                return redirect(destination)
            return redirect("index")
        else:
            context['signup_form'] = form
    return render(request, "accounts/register.html", context)

def logout_view(request):
    logout(request)
    return redirect("index")



def login_view(request,*args,**kwargs):
    context={}
    user = request.user
    if user.is_authenticated:
        return redirect('index')
    

    if request.POST:
        form = AccountAuthenticateForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email,password=password)
            if user:
                login(request,user)
                destination = get_redirect_if_exist(request)
                if destination:
                    return redirect(destination)
                return redirect('index')
        else:
            context['login_form'] = form   
    return render (request,'accounts/login.html',context)


def index(request):
    return render (request,'index.html')

def upload(request):
    return render (request,'accounts/upload.html')

def read_csv(request):
    data = pd.read_csv('static/fci-breeds.csv')
    specific_column=data["name"]
    context = {'loaded_data': specific_column}
    return render(request, "accounts/register.html", context)


def get_redirect_if_exist(request):
    redirect= None
    if request.GET:
        if request.GET.get("next") :
            redirect (str(request.GET.get("next")))
    return redirect

def account_view(request,*args,**kwargs):
    context={}
    user_id = kwargs.get("user_id")
    try:
        account = DogAccount.objects.get(pk=user_id)
    except DogAccount.DoesNotExist:
        return HttpResponse("Account Doesnt Exist")
    if account:
        context['id'] = account.id
        context['username'] = account.username
        context['email'] = account.email
        context['profile_image'] = account.profile_image.url
        context['hide_email'] = account.hide_email
    #state variables
        is_self=True
        is_friend = False
        user = request.user
        if user.is_authenticated and user != account:
            is_self = False
        elif not user.is_authenticated:
            is_self=False
        
        context['is_self'] = is_self
        context['is_friend'] = is_friend
        context['BASE_URL'] = settings.BASE_URL

        return render(request,"accounts/account.html",context)

# #@login_required()
# def upload(request):

#     if request.method == 'POST':
#         user = request.user.username
#         image = request.FILES.get('image_upload')
#         caption = request.POST['caption']

#         new_post = Post.objects.create(user=user, image=image, caption=caption)
#         new_post.save()

#         return redirect('/')
#     else:
#         return redirect('/')