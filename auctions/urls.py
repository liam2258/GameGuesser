from django.urls import path
from django.conf.urls import include

from . import views

# auctions/urls.py

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),
    path("contact/", views.contact, name="contact"),
    path("profile/", views.createProfile, name="profile")
]
