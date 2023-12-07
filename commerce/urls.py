"""commerce URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path

# commerce/urls.py

from django.contrib.sitemaps import GenericSitemap  # Importing sitemap generating library
from django.contrib.sitemaps.views import sitemap  # Importing sitemap generating function

from auctions.models import Listing  # Importing all Listing pages on our website

# Define the fields for the sitemap
info_dict = {
    "queryset": Listing.objects.filter(isActive=True), # Get all active listings
    "date_field": "updated_at", # Get the time the page was updated
}

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("auctions.urls")),

    # Create a url path for ever
    path(
        "sitemap.xml",
        sitemap, # Call sitemap generator and pass it the sitemap class filled by our dictionary
        {"sitemaps": {"auctions": GenericSitemap(info_dict)}},
    ),
]