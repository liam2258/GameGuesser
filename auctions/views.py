
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.views import PasswordResetView
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Profile, Scores
from .forms import ProfileForm

import requests
import random
import json
import environ

env = environ.Env()
environ.Env.read_env()
 
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
            user.backend = 'django.contrib.auth.backends.ModelBackend'
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

@login_required
def profile(request):
    profile_data, created = Profile.objects.get_or_create(user=request.user)
    return render(request, "auctions/profile.html", {"profile": profile_data})

def play(request):
    key = env('RAWG_API_KEY')
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

def gameOver(request):
    correct_guess_count = int(request.GET.get('correctGuessCount', 0))

    # Fetch the current user's score instance
    user_score, created = Scores.objects.get_or_create(user=request.user)

    # Check if the high_score attribute exists in the Scores model
    if correct_guess_count > user_score.high_score:
        user_score.high_score = correct_guess_count
        user_score.save()

    return render(request, "auctions/gameOver.html", {'user_score': user_score.high_score})

@login_required
def editProfile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("profile"))
        else:
            return render(request, "auctions/edit.html", {"form": form, "edit": profile})
    else:
        form = ProfileForm(instance=profile)

    return render(request, "auctions/edit.html", {"form": form, "edit": profile})

class YourPasswordResetView(PasswordResetView):
    template_name = 'auctions/reset_password.html'
    form_class = PasswordResetForm
    email_template_name = 'registration/password_reset_email.html'
    success_url = 'password_reset_done'


from operator import itemgetter

def scores(request):
    # Retrieve all Users along with their Scores
    users_with_scores = []
    all_users = User.objects.all()

    for user in all_users:
        # Retrieve the associated Scores for each User
        try:
            scores = Scores.objects.get(user=user)
        except Scores.DoesNotExist:
            scores = Scores(user=user, high_score=0)
            scores.save()

        users_with_scores.append({'user': user, 'scores': scores})

    # Sort the users_with_scores list by high_score
    users_with_scores.sort(key=lambda x: x['scores'].high_score, reverse=True)

    context = {
        'users_with_scores': users_with_scores
    }

    return render(request, 'auctions/scores.html', context)


