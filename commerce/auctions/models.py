from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinValueValidator

class User(AbstractUser):
    watchlist = models.ManyToManyField("Listing", blank=True, related_name="interested")

class Listing(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    startBid = models.IntegerField(default = 1, validators=[MinValueValidator(0)])
    category = models.CharField(max_length=100, blank=True)
    img = models.URLField(blank=True, max_length=1000)
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name="seller", default=0)
    active = models.BooleanField(default=True)
    winner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="winner", blank=True, null=True)

class Bid(models.Model):
    bid = models.IntegerField(default=1)
    Listingbids = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids", default=1)
    bidUser = models.ForeignKey(User, on_delete=models.CASCADE, default=1)

class Comment(models.Model):
    comment = models.CharField(max_length=1500, default="")
    commentListing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments", default=1)
    commentUser = models.ForeignKey(User, on_delete=models.CASCADE, related_name="commentUser", default=1)
