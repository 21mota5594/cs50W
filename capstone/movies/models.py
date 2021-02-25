from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    favorites = models.ManyToManyField("Movie", blank=True, related_name="favorites")
    recommended = models.ManyToManyField("Movie", blank=True, related_name="recommended")

class Movie(models.Model):
    title = models.CharField(max_length=150)
    imgUrl = models.URLField(max_length=1500, default="https://sainfoinc.com/wp-content/uploads/2018/02/image-not-available.jpg")
    imbdID = models.CharField(max_length=50, null=True, blank=True)

