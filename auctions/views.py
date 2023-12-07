# You are awesome
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Category, Listing, Comment, Bid

# auctions/views.py

from django.shortcuts import render, get_object_or_404
from django.views import View
from .models import Listing

class ListingDetailView(View):
    template_name = 'auctions/listing_detail.html'

    def get(self, request, pk):
        listing = get_object_or_404(Listing, pk=pk)
        return render(request, self.template_name, {'listing': listing})

def listing(request, id):
    listingData = Listing.objects.get(pk=id)
    isListingInWatchList = request.user in listingData.watchlist.all()
    allComments = Comment.objects.filter(listing=listingData)
    isOwner = request.user.username == listingData.owner.username
    return render(request, "auctions/listing.html", {
        "listing": listingData,
        "isListingInWatchList" : isListingInWatchList,
        "allComments": allComments,
        "isOwner": isOwner
    })

def categories(request):
    categories = Category.objects.values_list('categoryName', flat=True).distinct()

    categories = list(categories)
    print(categories)

    return render(request, "auctions/categories.html", {
        "categories": categories
    })

def categoryList(request, category):
    # Filter the listings by category
    listings = Listing.objects.filter(category=category)

    return render(request, "auctions/categoryList.html", {
        "category": category,
        "listings": listings
    })

def closeAuction(request, id):
    listingData = Listing.objects.get(pk=id)
    listingData.isActive = False
    listingData.save()
    isListingInWatchList = request.user in listingData.watchlist.all()
    allComments = Comment.objects.filter(listing=listingData)
    isOwner = request.user.username == listingData.owner.username
    return render(request, "auctions/listing.html", {
        "listing": listingData,
        "isListingInWatchList" : isListingInWatchList,
        "allComments": allComments,
        "isOwner": isOwner, 
        "update": True,
        "message": "Auction closed"
    })

def addBid(request, id):
    newBid = request.POST['newBid']
    listingData = Listing.objects.get(pk=id)
    isListingInWatchList = request.user in listingData.watchlist.all()
    allComments = Comment.objects.filter(listing=listingData)
    isOwner = request.user.username == listingData.owner.username
    if float(newBid) > float(listingData.price.bid):
        updateBid = Bid(user=request.user, bid=float(newBid))
        updateBid.save()
        listingData.price = updateBid
        listingData.save()
        return render(request, "auctions/listing.html", {
            "listing": listingData,
            "message": "Successful bid",
            "update": True,
            "isListingInWatchList" : isListingInWatchList,
            "allComments": allComments,
            "isOwner": isOwner, 
        })
    else:
        return render(request, "auctions/listing.html", {
            "listing": listingData,
            "message": "Unsuccessful bid",
            "update": False,
            "isListingInWatchList" : isListingInWatchList,
            "allComments": allComments,
            "isOwner": isOwner, 
        })

from django.http import JsonResponse

def addComment(request, id):
    currentUser = request.user
    listingData = Listing.objects.get(pk=id)
    message = request.POST['comment']

    newComment = Comment(
        author=currentUser,
        listing=listingData,
        message=message
    )

    newComment.save()

    # Return the new comment details as JSON
    return JsonResponse({
        'author': newComment.author.username,
        'message': newComment.message
    })


def displayWatchList(request):
    currentUser = request.user
    listings = currentUser.listingWatchList.all()
    print(listings)
    return render(request, "auctions/watchlist.html", {
        "listings": listings
    })

'''def removeWatchList(request, id):
    listingData = Listing.objects.get(pk=id)
    currentUser = request.user
    listingData.watchlist.remove(currentUser)
    return HttpResponseRedirect(reverse("listing", args=(id, )))

def addWatchList(request, id):
    listingData = Listing.objects.get(pk=id)
    currentUser = request.user
    listingData.watchlist.add(currentUser)
    return HttpResponseRedirect(reverse("listing", args=(id, )))'''
def removeWatchList(request, id):
    try:
        listingData = Listing.objects.get(pk=id)
        currentUser = request.user
        listingData.watchlist.remove(currentUser)
        return JsonResponse({'success': True})
    except Listing.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Listing does not exist'}, status=404)

def addWatchList(request, id):
    try:
        listingData = Listing.objects.get(pk=id)
        currentUser = request.user
        listingData.watchlist.add(currentUser)
        return JsonResponse({'success': True})
    except Listing.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Listing does not exist'}, status=404)
    
def index(request):
    activeListings = Listing.objects.filter(isActive=True)
    allCategories = Category.objects.all()
    return render(request, "auctions/index.html", {
        "listings": activeListings,
        "categories": allCategories
    })

def displayCategory(request):
    print(request.POST)
    if request.method == "POST":
        categoryFromForm = request.POST['category']
        category = Category.objects.get(categoryName=categoryFromForm)
        activeListings = Listing.objects.filter(isActive=True, category=category)
        allCategories = Category.objects.all()
    return render(request, "auctions/index.html", {
        "listings": activeListings,
        "categories": allCategories
    })

    pass

def createListing(request):
    if request.method == "GET":
        allCategories = Category.objects.all()
        return render(request, "auctions/create.html", {
            "categories": allCategories
        })
    else:
        print(request.POST)
        title = request.POST["title"]
        description = request.POST["description"]
        imageurl = request.POST["imageurl"]
        price = request.POST["price"]
        category = request.POST["category"]

        currentUser = request.user

        categoryData = Category.objects.get(categoryName=category)

        bid = Bid(bid=float(price), user=currentUser)
        bid.save()

        newListing = Listing(
            title=title,
            description=description,
            imageUrl=imageurl,
            price=bid,
            category=categoryData,
            owner=currentUser
        )

        newListing.save()

        return HttpResponseRedirect(reverse(index))


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

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
    
