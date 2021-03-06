
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("feed", views.following, name="following"),
    

    path("post", views.post, name="post"),
    path("follow/<str:username>", views.follow, name="follow"),
    path("edit", views.edit, name="edit"),
    path("like", views.like, name="like"),

    path("<str:username>", views.profile, name="profile")
]
