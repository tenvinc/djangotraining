from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import AdminUser, Student, CustomUser


class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']


class AdminRegistrationForm(forms.ModelForm):
    class Meta:
        model = AdminUser
        fields = ['full_name']


class StudentRegistrationForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['full_name','course', 'year_of_study', 'weight', 'height', 'age']


class StudentUpdateForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['course', 'year_of_study', 'weight', 'height', 'age']