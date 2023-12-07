from django.urls import path
from django.conf.urls import include

from . import views
from .views import ListingDetailView

# auctions/urls.py

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),
    path("create/", views.createListing, name="create"),
    path("displayCategory/", views.displayCategory, name="displayCategory"),
    path('listing/<int:id>/', views.listing, name='listing'),
    path('removeWatchList/<int:id>/', views.removeWatchList, name='removeWatchList'),
    path('addWatchList/<int:id>/', views.addWatchList, name='addWatchList'),
    path('watchlist/', views.displayWatchList, name='watchlist'),
    path('addComment/<int:id>/', views.addComment, name='addComment'),
    path('addBid/<int:id>/', views.addBid, name='addBid'),
    path('closeAuction/<int:id>/', views.closeAuction, name='closeAuction'),
    path('categories', views.categories, name='categories'),
    path('categoryList/<str:category>/', views.categoryList, name='categoryList'),
    path('oauth/', include('social_django.urls', namespace='social')), # here we add the URL

    # Use our path to get to view function and pass it the page id
    path('listing/<int:pk>/', ListingDetailView.as_view(), name='listing_detail'),
]
