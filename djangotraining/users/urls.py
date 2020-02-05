from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'register/$', views.register, name='register'),
    url(r'login/$', views.CustomLoginView.as_view(), name='login'),
    url(r'logout/$', auth_views.LogoutView.as_view(template_name="users/logout.html"), name='logout'),
    url(r'main/$', views.MainPageView.as_view(), name="site-main"),
    url(r'admin/$', views.AdminView.as_view(), name="site-admin"),
    url(r'profile/$', views.ProfileView.as_view(), name='user-profile'),
    url(r'profile/(?P<pk>[0-9]+)/$', views.ProfileView.as_view(), name='user-profile'),
    url(r'profile/update/$', views.ProfileUpdateView.as_view(), name='profile-update'),
    url(r'profile/update/(?P<pk>[0-9]+)/$', views.ProfileUpdateView.as_view(), name='profile-update'),
    url(r'test/$', views.TestView.as_view(), name='user-test'),
    url(r'^', views.home, name='users-home'),
]
