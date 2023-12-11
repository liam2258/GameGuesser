from django.urls import path
from django.conf.urls import include
from django.contrib.auth import views as auth_views

from . import views

# auctions/urls.py

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),
    path("contact/", views.contact, name="contact"),
    path("profile/", views.profile, name="profile"),
    path("edit/", views.editProfile, name="edit"),
    path("scores/", views.scores, name="scores"),
    path("play/", views.play, name="play"),

    path('reset_password/', auth_views.PasswordResetView.as_view(), name='reset_password'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    
    
]
