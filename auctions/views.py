
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.views import PasswordResetView
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from .models import User, Profile, Scores
from .forms import ProfileForm

import requests
import random
import json
 
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
    
def contact(request):
    return render(request, "auctions/contact.html")

def reset(request):
    return render(request, "auctions/reset.html")

def profile(request):
    profile_data = Profile.objects.first()
    return render(request, "auctions/profile.html", {"profile": profile_data})

def play(request):
    key = '24ba40af039341fdb5fe051e64faa314'
    page = 1
    r = requests.get(f"https://api.rawg.io/api/games?key={key}&page={page}")

    data = r.json()

    titles = []
    scores = []
    releases = []
    images = []

    for game in data['results']:
        if game['metacritic'] and game['background_image']:
            titles.append(game['name'])
            scores.append(game['metacritic'])
            releases.append(game['released'][:4])
            images.append(game['background_image'])

    gameList = [
        {"title": title, "score": score, "release": release, "image": image}
        for title, score, release, image in zip(titles, scores, releases, images)
    ]

    # Randomize the order of games
    random.shuffle(gameList)

    gameList = json.dumps(gameList)

    # Pass the gameList to the template
    return render(request, "auctions/play.html", {"gameList": gameList})

# def editProfile(request):
#     profile = get_object_or_404(Profile, pk=1)  # Assuming there's only one profile object

#     if request.method == "POST":
#         form = ProfileForm(request.POST, request.FILES, instance=profile)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect(reverse("profile"))
#     else:
#         form = ProfileForm(instance=profile)

#     return render(request, "auctions/edit.html", {"form": form, "edit": profile})
login_required
def editProfile(request):
    profile = Profile.objects.first()  # Or fetch the specific profile you want to edit

    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("profile"))
    else:
        form = ProfileForm(instance=profile)

    return render(request, "auctions/edit.html", {"form": form, "edit": profile})


class YourPasswordResetView(PasswordResetView):
    template_name = 'auctions/reset_password.html'
    form_class = PasswordResetForm
    email_template_name = 'registration/password_reset_email.html'
    success_url = 'password_reset_done'  # Make sure to adjust the success URL as needed

from django.shortcuts import render
from .models import User, Scores  # Import your models

def scores(request):
    # Retrieve all Users along with their Scores
    users_with_scores = []
    all_users = User.objects.all()

    for user in all_users:
        # Retrieve the associated Scores for each User
        try:
            scores = Scores.objects.get(user=user)
        except Scores.DoesNotExist:
            scores = 0

        users_with_scores.append({'user': user, 'scores': scores})

    context = {
        'users_with_scores': users_with_scores
    }
    users_with_scores = Scores.objects.select_related('user').order_by('-high_score')
    return render(request, 'auctions/scores.html', context)


