from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
import requests
import json

from .models import User, Movie

# Create your views here.
def index(request):
    user = request.user
    try:
        favorites = user.favorites.all()
        favNum = favorites.count()
    except AttributeError:
        favorites = []
        favNum = 0
    
    rnge = 5 - favNum

    try:
        recommended = user.recommended.all()
    except User.DoesNotExist:
        recommended = {}
    return render(request, 'movies/index.html', {
        "range": range(rnge),
        "favorites": favorites,
        "recommended": recommended
    })

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "movies/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "movies/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "movies/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password) 
            user.save()
        except IntegrityError:
            return render(request, "movies/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "movies/register.html")

def movieSearch(request):
    movie = {}
    movie["title"] = "Gladiator"
    movie["img"] = "https://m.media-amazon.com/images/M/MV5BMDliMmNhNDEtODUyOS00MjNlLTgxODEtN2U3NzIxMGVkZTA1L2ltYWdlXkEyXkFqcGdeQXVyNjU0OTQ0OTY@._V1_.jpg"
    movie["stars"] = ["Russell Crowe", "Joaquin Phoenix"]

    if Movie.objects.filter(title=movie["title"]).exists():
            movieObj = Movie.objects.get(title=movie["title"])
    else:
        movieObj = ""
    return render(request, "movies/movie.html", {
        "movie": movie,
        "moveiObj": movieObj
        
    })
    if request.GET.get('q') is not None:
        query = request.GET.get('q')

        url = "https://imdb8.p.rapidapi.com/title/find"

        querystring = {"q": query}

        headers = {
                    'x-rapidapi-key': "390b7de26dmshbdd593d0fd46ee9p1a9b5djsnb68cbab19b3f",
                    'x-rapidapi-host': "imdb8.p.rapidapi.com"
                    }

        response = requests.request("GET", url, headers=headers, params=querystring)

        response = response.json()

        id = response["results"][0]["id"]
        title = response["results"][0]["title"]
        img = response["results"][0]["image"]["url"]
        year = response["result"][0]["year"]

        movie = {}
        movie["title"] = title
        movie["img"] = img
        movie["year"] = year
        movie["id"] = id
        return render(request, "movies/movie.html", {
            "movie": movie,            
        })


@csrf_exempt
def favorite(request):
    if request.method == "PUT":
        # check action
        data = json.loads(request.body)
        action = data.get('action')
        title = data.get('title')
        url = data.get('url')
        id = data.get('id')
        id = id.split("/")
        id = id[2]
        user = request.user
        if Movie.objects.filter(title=title).exists():
            movie = Movie.objects.get(title=title)
        else:
            Movie.objects.create(title=title, imgUrl=url, imbdID=id)
        if action == "favorite":
            user.favorites.add(movie)
        else:
            user.favorites.remove(movie)
        return JsonResponse({"message": "Action complete"}, status=201)

def removeFavorite(request, title):
    movie = Movie.objects.get(title=title)
    request.user.favorites.remove(movie)

    return HttpResponseRedirect(reverse("index"))

def community(request):
    return render(request, "movies/community.html", {
        "users": User.objects.all()
    })

def recommend(request):
    user = request.user

    favorites = user.favorites.all()
    recID = []

    for favorite in favorites:
        favorite.imbdID = favorite.imbdID.split("/")
        favorite.imbdID = favorite.imbdID[2]
        url = "https://imdb8.p.rapidapi.com/title/get-more-like-this"

        querystring = {"tconst":favorite.imbdID,"currentCountry":"US","purchaseCountry":"US"}

        headers = {
            'x-rapidapi-key': "390b7de26dmshbdd593d0fd46ee9p1a9b5djsnb68cbab19b3f",
            'x-rapidapi-host': "imdb8.p.rapidapi.com"
            }

        response = requests.request("GET", url, headers=headers, params=querystring)
        response = response.json()
        recID.append(response[0])

    for id in recID:
        id = id.split("/")
        id = id[2]
        url = "https://imdb8.p.rapidapi.com/title/get-base"

        querystring = {"tconst":id}

        headers = {
            'x-rapidapi-key': "390b7de26dmshbdd593d0fd46ee9p1a9b5djsnb68cbab19b3f",
            'x-rapidapi-host': "imdb8.p.rapidapi.com"
            }

        response = requests.request("GET", url, headers=headers, params=querystring)

        response = response.json()
        
        id = response["id"]
        title = response["title"]
        url = response["image"]["url"]
        year = response["year"]

        movie = Movie.objects.create(title=title, imgUrl=url, imbdID=id)
        movie.save()
        user.recommended.add(movie)


    if len(recID) != 5:
        # what happens if recommendation is repeated?
        # have to set recID to list(set(recID))
        movie = favorites.first()
        for i in 5 - len(recID):
            pass
    
    favorites = user.favorites.all()
    recommended = user.recommended.all()

    return render(request, 'movies/index.html', {
        "range": range(0),
        "favorites": favorites,
        "recommended": recommended
    })

