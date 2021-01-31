from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("listing/<int:id>", views.listing, name="listing"),
    path("addwatchlist/<int:id>", views.addwatchlist, name="addwatchlist"),
    path("closeListing/<int:id>", views.closeListing, name="closeListing"),
    path("comment/<int:id>", views.comment, name="comment"),
    path("watchlist/<int:id>", views.watchlist, name="watchlist"),
    path("category/<str:category>", views.category, name="category"),
    path("categories", views.categories, name="categories")
    
]
