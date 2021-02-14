from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Post, UserFollowing

# Register your models here.
admin.site.register(User)
admin.site.register(UserFollowing)
admin.site.register(Post)