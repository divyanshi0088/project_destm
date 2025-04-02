from django.urls import path
from django.shortcuts import render

from .views import register_user, login_user, user_dashboard
def register_page(request):
    return render(request, "register.html")

def login_page(request):
    return render(request, "login.html")

def dashboard_page(request):
    return render(request, "dashboard.html")

urlpatterns = [
    path("register/", register_page, name="register_page"),
    path("login/", login_page, name="login_page"),
    path("dashboard/", dashboard_page, name="dashboard_page"),
    #endpoints urls
    path("api/register/", register_user, name="api_register"),
    path("api/login/", login_user, name="api_login"),
    path("api/dashboard/", user_dashboard, name="api_dashboard"),
]