from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass
    

class Post(models.Model):
    post = models.CharField(max_length=1000)
    poster = models.ForeignKey(User, on_delete=models.CASCADE, related_name="poster")
    likes = models.IntegerField(default=0)
    likers = models.ForeignKey(User, on_delete=models.CASCADE, related_name="likers", blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def serialize(self):
        return {
            "id": self.id,
            "post": self.post,
            "poster": self.poster.username,
            "likes": self.likes,
            "timestamp": self.timestamp.strftime("%b %-d %Y, %-I:%M %p")
        }

class UserFollowing(models.Model):
    userId = models.ForeignKey("User", related_name="following", on_delete=models.DO_NOTHING, null=True)
    followingUserId = models.ForeignKey("User", related_name="followers", on_delete=models.DO_NOTHING, null=True)