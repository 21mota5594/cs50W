from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("movieSearch", views.movieSearch, name="movieSearch"),
    path("community", views.community, name="community"),
    path("recommend", views.recommend, name="recommend"),

    path("favorite", views.favorite, name="favorite"),
    path("removeFavorite/<str:title>", views.removeFavorite, name="removeFavorite")
]