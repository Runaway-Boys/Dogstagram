from django.contrib.auth import  login, logout,authenticate
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.conf import settings
from django.core.files.storage import default_storage,FileSystemStorage
from django.core import files

import os
import cv2
import json
import base64
from joblib import load
import tensorflow as tf
from accounts.forms import AccountUpdateForm,SignupForm,AccountAuthenticateForm
from accounts.models import DogAccount
import warnings
from keras.preprocessing.image import load_img
import numpy as np
from django.contrib import messages
warnings.filterwarnings('ignore')
import pandas as pd

TEMP_PROFILE_IMAGE_NAME ="temp_profile_image.png"
import tensorflow as tf
from tensorflow import keras
# Recreate the exact same model, including its weights and the optimizer
new_model = tf.keras.models.load_model('models/Dog-Model.h5')


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
    
    context = {}
    user_id = kwargs.get("user_id")
    try:
        account = DogAccount.objects.get(pk=user_id)
    except:
        return HttpResponse("Something went wrong.")
    if account:
        context['id'] = account.id
        context['username'] = account.username
        context['email'] = account.email
        context['profile_image'] = account.profile_image.url
        context['hide_email'] = account.hide_email

        # Define template variables
        is_self = True
        is_friend = False
        user = request.user
        if user.is_authenticated and user != account:
            is_self = False
        elif not user.is_authenticated:
            is_self = False
            
        # Set the template variables to the values
        context['is_self'] = is_self
        context['is_friend'] = is_friend
        context['BASE_URL'] = settings.BASE_URL

        return render(request,"accounts/account.html",context)

def account_search_view(request, *args, **kwargs):
	context = {}
	if request.method == "GET":
		search_query = request.GET.get("q")
		if len(search_query) > 0:
			search_results = DogAccount.objects.filter(email__icontains=search_query).filter(username__icontains=search_query).distinct()
			accounts = [] # [(account1, True), (account2, False), ...]
			for account in search_results:
				accounts.append((account, False)) # you have no friends yet
			context['accounts'] = accounts
				
	return render(request, "accounts/search_results.html", context)
            
def edit_account_view(request,*args,**kwargs):
	if not request.user.is_authenticated:
		return redirect("login")
	user_id = kwargs.get("user_id")
	account = DogAccount.objects.get(pk=user_id)
	if account.pk != request.user.pk:
		return HttpResponse("You cannot edit someone elses profile.")
	context = {}
	if request.POST:
		form = AccountUpdateForm(request.POST, request.FILES, instance=request.user)
		if form.is_valid():
                  
			form.save()
			return redirect("accounts:view", user_id=account.pk)
		else:
			form = AccountUpdateForm(request.POST, instance=request.user,
				initial={
					"id": account.pk,
					"email": account.email, 
					"username": account.username,
					"profile_image": account.profile_image,
					"hide_email": account.hide_email,
				}
			)
			context['form'] = form
	else:
		form = AccountUpdateForm(
			initial={
					"id": account.pk,
					"email": account.email, 
					"username": account.username,
					"profile_image": account.profile_image,
					"hide_email": account.hide_email,
				}
			)
		context['form'] = form
          #set limits to the size of the image upload
	context['DATA_UPLOAD_MAX_MEMORY_SIZE'] = settings.DATA_UPLOAD_MAX_MEMORY_SIZE
	return render(request, "accounts/edit_account.html", context)     


def save_temp_profile_image_from_base64String(imageString, user):

	INCORRECT_PADDING_EXCEPTION = "Incorrect padding"
	try:
		if not os.path.exists(settings.TEMP):
			os.mkdir(settings.TEMP)
		if not os.path.exists(settings.TEMP + "/" + str(user.pk)):
			os.mkdir(settings.TEMP + "/" + str(user.pk))
		url = os.path.join(settings.TEMP + "/" + str(user.pk),TEMP_PROFILE_IMAGE_NAME)
		storage = FileSystemStorage(location=url)    

            
		image = base64.b64decode(imageString)
		
		with storage.open('', 'wb+') as destination:
			destination.write(image)
			destination.close()
		return url
	except Exception as e:
		print("exception: " + str(e))
		# workaround for an issue I found
		if str(e) == INCORRECT_PADDING_EXCEPTION:
			imageString += "=" * ((4 - len(imageString) % 4) % 4)
			return save_temp_profile_image_from_base64String(imageString, user)
	return None

def crop_image(request, *args, **kwargs):
	payload = {}
	user = request.user
	if request.POST and user.is_authenticated:
		try:
			imageString = request.POST.get("image")
			
			url = save_temp_profile_image_from_base64String(imageString, user)
			img = cv2.imread(url)
			

			cropX = int(float(str(request.POST.get("cropX"))))
			cropY = int(float(str(request.POST.get("cropY"))))
			cropWidth = int(float(str(request.POST.get("cropWidth"))))
			cropHeight = int(float(str(request.POST.get("cropHeight"))))
			if cropX < 0:
				cropX = 0
			if cropY < 0: # There is a bug with cropperjs. y can be negative.
				cropY = 0
			crop_img = img[cropY:cropY+cropHeight, cropX:cropX+cropWidth]

			cv2.imwrite(url, crop_img)

			
			

			
			
			#model that determines if the pic is a dog
			save = url
			img = load_img(save, target_size=(128, 128))
			img = np.array(img)
			img = img / 255.0 # normalize the image
			img = img.reshape(1, 128, 128, 3) # reshape for prediction
			pred = new_model.predict(img)
                  #if dog
			if pred[0] > 0.5:
                        # delete the old image
				print("dog")
				user.profile_image.delete()
                        # Save the cropped image to user model
				user.profile_image.save("profile_image.png", files.File(open(url, 'rb')))
				user.save()

				payload['result'] = "success"
				payload['cropped_profile_image'] = user.profile_image.url

				# delete temp file
				os.remove(url)
				#if not dog
			else:
				print("not Dog")
				messages.info(request, 'Hey Thats Not a Dog!!!')
					
                        # Save the cropped image to user model
				
				user.save()

				payload['result'] = "success"
				payload['cropped_profile_image'] = user.profile_image.url

				# delete temp file
				os.remove(url)        				
			# user.save()

			# payload['result'] = "success"
			# payload['cropped_profile_image'] = user.profile_image.url

			# # delete temp file
			# os.remove(url)
			
		except Exception as e:
			print("exception: " + str(e))
			payload['result'] = "error"
			payload['exception'] = str(e)
	return HttpResponse(json.dumps(payload), content_type="application/json")
