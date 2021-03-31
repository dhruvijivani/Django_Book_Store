from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views
urlpatterns = [
    
    path("signup", views.signup, name='signup'),
    path("login", views.login, name="login"),
    path("main1", views.main1, name="main1"),
    path("profile", views.profile, name="profile"),
    path("logout", views.logout, name="logout"),
    path("search", views.search, name="search"),
    # path('reset_password/', auth_views.PasswordResetView.as_view()),

]
