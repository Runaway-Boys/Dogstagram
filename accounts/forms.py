
from django.contrib.auth.forms import UserCreationForm
from .models import DogAccount
from django import forms

class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=255,help_text="required. Add a valid email address ... ")
    class Meta:
        model = DogAccount
        fields = ['email','username','password1','password2']

    def clean_email(self):
        email = self.changed_data['email'].lower()
        try:
            account = DogAccount.objects.get(email=email)
        except Exception as e:
            return email

        raise forms.ValidationError(f'Email{email} is already in use')

    def clean_username(self):
            username = self.changed_data['username']
            try:
                account = DogAccount.objects.get(username=username)
            except Exception as e:
                return username

            raise forms.ValidationError(f'UserName{username} is already in use')
