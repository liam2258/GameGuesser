
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User
from .forms import ProfileForm
 
def index(request):
   return render(request, "auctions/index.html")

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]

        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        try:
            user = User.objects.create_user(username, email, password)
            user.backend = 'django.contrib.auth.backends.ModelBackend'  # Set the backend
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })

        authenticated_user = authenticate(request, username=username, password=password)
        if authenticated_user is not None:
            login(request, authenticated_user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Failed to log in the user."
            })
    else:
        return render(request, "auctions/register.html")
    
def profile(request):
    return render(request, "auctions/profile.html")

def contact(request):
    return render(request, "auctions/contact.html")

def reset(request):
    return render(request, "auctions/reset.html")

def createProfile(request):
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("profile"))
    else:
        form = ProfileForm()

    return render(request, "auctions/profile.html", {"form": form})

from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.views import PasswordResetView

class YourPasswordResetView(PasswordResetView):
    template_name = 'auctions/reset_password.html'
    form_class = PasswordResetForm
    email_template_name = 'registration/password_reset_email.html'
    success_url = 'password_reset_done'  # Make sure to adjust the success URL as needed