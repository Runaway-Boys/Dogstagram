from django.contrib.auth import  login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.shortcuts import render, redirect
from django.http import HttpResponse
# Create your views here.

def register_view(request):
    form = UserCreationForm(request.POST or None)
    if form.is_valid():
        return redirect('/login')
    context = {"form": form}
    return render(request, "accounts/register.html", context)


def login_view(request):
    return render (request,'accounts/login.html')


def index(request):
    return render (request,'index.html')

def upload(request):
    return render (request,'accounts/upload.html')

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