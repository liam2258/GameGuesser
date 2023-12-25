from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings


class User(AbstractUser):
    pass

class Scores(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="user_score")
    high_score = models.IntegerField(default=0)

class Category(models.Model):
    categoryName = models.CharField(max_length=60)

    def __str__(self):
        return self.categoryName

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="user_profile", null=True, blank=True)
    image = models.ImageField(upload_to='profile_images')
    avatar = models.CharField(max_length=50)
    about = models.CharField(max_length=150)

    def __str__(self):
        return self.avatar

    @property
    def email(self):
        return self.user.email if self.user else None

    