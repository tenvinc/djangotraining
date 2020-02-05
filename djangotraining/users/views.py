# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.template import loader
from django.contrib import messages
from django.views import View
from django.views.generic import ListView
from django.views.generic.edit import FormMixin, TemplateResponseMixin
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin

from django.core.exceptions import PermissionDenied

from .forms import AdminRegistrationForm, StudentRegistrationForm, UserRegistrationForm, StudentUpdateForm
from .models import AdminUser, Student


# Create your views here.
def home(request):
    user = request.user
    if not user is None and user.is_authenticated:
        print("User authenticated. Skipping pre-login page...")
        return redirect('site-main')
    print("User not authenticated. Going to pre-login page...")
    return render(request, 'users/home.html')


def register(request):
    if request.method == "POST":
        print("New post request submitted")
        u_form = UserRegistrationForm(request.POST, prefix='user')
        a_form = AdminRegistrationForm(request.POST, prefix='admin')
        if u_form.is_valid() and a_form.is_valid():
            user = u_form.save(commit=False)
            user.is_manager = True
            user.save()
            admin = a_form.save(commit=False)
            admin.user = user
            admin.save()
            messages.success(request, "{} successfully created.".format(admin))
            return redirect('site-main')
        else:
            print("Form post request is invalid. Trying again...")
    
    else:
        u_form = UserRegistrationForm(prefix='user')
        a_form = AdminRegistrationForm(prefix='admin')
    
    context = {
        'u_form': u_form,
        'a_form': a_form
    }

    return render(request, 'users/register.html', context)


class CustomLoginView(LoginView):
    template_name = 'users/login.html' 

    def form_valid(self, form):
        """Security check complete. Log the user in."""
        print("User logging in".format(form.get_user()))
        return super(CustomLoginView, self).form_valid(form)

    def get(self, request, *args, **kwargs):
        return self.render_to_response(self.get_context_data())

    def post(self, request, *args, **kwargs):
        """
        Handles POST requests, instantiating a form instance with the passed
        POST variables and then checked for validity.
        """
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
        

class MainPageView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        context = {}
        registered_students = Student.objects.all()
        context['registered_students'] = registered_students
        for student in registered_students:
            print(student.pk)
        print(context)
        return render(request, 'users/main.html', context=context)


class AdminView(LoginRequiredMixin, TemplateResponseMixin, View):
    template_name = 'users/admin.html'

    def get(self, request, *args, **kwargs):
        active_user = request.user
        if not active_user.is_manager:
            print("User does not have adequate permissions.")
            raise PermissionDenied
        context = {
            'is_admin': active_user.is_manager
        }
        u_form = UserRegistrationForm(prefix="user")
        s_form = StudentRegistrationForm(prefix="student")
        context['u_form'] = u_form
        context['s_form'] = s_form

        return render(request, self.template_name, context=context)

    def post(self, request, *args, **kwargs):
        u_form = UserRegistrationForm(request.POST, prefix="user")
        s_form = StudentRegistrationForm(request.POST, prefix="student")

        if u_form.is_valid() and s_form.is_valid():
            return self.form_valid(u_form, s_form)
        else:
            return self.form_invalid(u_form, s_form)
  
    def form_valid(self, u_form, s_form):
        user = u_form.save(commit=False)
        user.is_student = True
        user.save()
        student = s_form.save(commit=False)
        student.user = user
        student.save()
        print("Finished creating new student account {}".format(student.user.username))
        s_form = StudentRegistrationForm()
        u_form = UserRegistrationForm()
        context = {'s_form': s_form, 'u_form':u_form}
        messages.success(self.request, "{} successfully created.".format(student))
        return render(self.request, self.template_name, context=context)

    def form_invalid(self, u_form, s_form):
        print("Invalid form, try again")
        return render(self.request, self.template_name, context={'u_form': u_form, 's_form': s_form})


class ProfileView(LoginRequiredMixin, View):
    def get(self, request, pk=None, *args, **kwargs):
        user_to_show = None
        active_user = request.user  # Current user logged in
        if not pk is None:
            pk = int(pk)
            user_to_show = Student.objects.get(pk=pk).user
        else:
            user_to_show = request.user
        context = {}
        context['user_to_show'] = user_to_show
        if user_to_show.is_student:
            context['profile'] = user_to_show.student
        elif user_to_show.is_manager:
            context['profile'] = user_to_show.adminuser
        context['same_person'] = user_to_show == active_user
        return render(request, 'users/profile.html', context=context)


class ProfileUpdateView(LoginRequiredMixin, View):
    def get(self, request, pk=None, *args, **kwargs):
        user_to_show = None
        active_user = request.user  # Current user logged in
        if not pk is None:
            user_to_show = Student.objects.get(pk=pk).user
        else:
            user_to_show = request.user
        context = {}
        context['user_to_show'] = user_to_show
        if user_to_show.is_student:
            context['profile'] = user_to_show.student
            s_form = StudentUpdateForm(instance=user_to_show.student)
            context['s_form'] = s_form
        if user_to_show.is_manager:
            context['profile'] = user_to_show.adminuser
        return render(request, 'users/profile_update.html', context=context)
    
    def post(self, request, pk=None, *args, **kwargs):
        user_to_show = None
        if not pk is None:
            pk = int(pk)
            user_to_show = Student.objects.get(pk=pk).user
            pk = str(pk)
        else:
            pk = ""
            user_to_show = request.user
        active_user = request.user
        if user_to_show.is_manager:
            return redirect('user-profile')
        s_form = StudentUpdateForm(request.POST, instance=user_to_show.student)
        if s_form.is_valid():
            return self.form_valid(s_form, pk=pk)
        else:
            return self.form_invalid(s_form)
    
    def form_valid(self, s_form, pk=""):
        student = s_form.save()
        print("Finished updating student account {}".format(student.user.username))
        messages.success(self.request, "Profile successfully updated.")
        return redirect('user-profile') if pk == "" else redirect('user-profile', pk=pk)

    def form_invalid(self, s_form):
        print("Invalid form, try again")
        return render(self.request, self.template_name, context={'s_form': s_form})


class TestView(View):
    def get(self, request, *args, **kwargs):
        print("here")
        form = UserRegistrationForm()
        context = {'form': form}
        return render(request, 'users/test.html', context=context)