from django.contrib.auth import  login, logout,authenticate
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.shortcuts import render, redirect
from django.http import HttpResponse
from accounts.forms import SignupForm


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
            destination = kwargs.get("next")
            if destination:
                return redirect(destination)
            return redirect("index")
        else:
            context['signup_form'] = form
    return render(request, "accounts/register.html", context)


def login_view(request):
    return render (request,'accounts/login.html')


def index(request):
    return render (request,'index.html')

def upload(request):
    return render (request,'accounts/upload.html')

def read_csv(request):
    data = pd.read_csv('static/fci-breeds.csv')
    specific_column=data["name"]
    context = {'loaded_data': specific_column}
    return render(request, "accounts/register.html", context)
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