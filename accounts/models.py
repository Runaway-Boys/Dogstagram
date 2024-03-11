from django.db import models

from django.contrib.auth.models import AbstractBaseUser,BaseUserManager
# Create your models here.



class AccountManager(BaseUserManager):
    def create_user(self,email,username,password=None):
        if not email:
            raise ValueError("Email required")
        if not username:
            raise ValueError("Username is required")
        user = self.model(
            email=self.normalize_email(email),
            username=username,

        )
        user.set_password(password)
        user.save(using=self._db)
        return user

#create a superuser
    def create_superuser(self,email,username,password):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password,
        )
        user.is_admin=True
        user.is_staff=True
        user.is_superuser = True
        user.save(using=self._db)
        return user 
def get_profile_image_filepath(self,filename):
    return f'profile_images/{self.pk}/{"profile_image.png"}'

def get_default_profile_image():
    return "medias/default-dog-profile.png"


class DogAccount(AbstractBaseUser):
    email =  models.EmailField(verbose_name = "email", max_length=60,unique=True,blank= True)
    username = models.CharField(max_length=30,unique=True,null = True)
    bio = models.TextField(max_length=255,blank=True)
    date_joined = models.DateTimeField(verbose_name="date joined", auto_now_add=True)
    profile_image = models.ImageField(max_length=255,blank = True,null =True,upload_to=get_profile_image_filepath, default= get_default_profile_image)
    location = models.CharField(max_length=100, blank=True)
    
    
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    hide_email = models.BooleanField(default = True)

    objects = AccountManager()

    USERNAME_FIELD = "email" 
    REQUIRED_FIELDS = ['username']



    def __str__(self):
        return self.username
    
    def get_profile_image(self):
        return str(self.profile_image)[str(self.profile_image).index(f'profile_images/{self.pk}/'):]

    def has_perm(self,perm,obj=None):
        return self.is_admin
    
    def has_module_perms(self,app_label):
        return True