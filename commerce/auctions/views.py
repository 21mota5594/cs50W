from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Max
from PIL import Image

from .models import User, Listing, Bid, Comment


def index(request):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.all()
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
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


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
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


@login_required
def create(request):
    if request.method == 'POST':
        title = request.POST["title"]
        description = request.POST["description"]
        startBid = request.POST["startBid"]
        category = request.POST["category"]
        img = request.POST["image"]
        seller = request.user

        listing = Listing.objects.create(title=title, description=description, startBid=startBid, category=category, img=img, seller=seller)
        listing.save()
        messages.success(request, 'Listing added successfully')
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, 'auctions/create.html')

def listing(request, id):
    listing = Listing.objects.get(pk=id)
    allBids = listing.bids.all()
    if request.method == 'POST':
        bid = int(request.POST["bid"])
        highestBid = allBids.all().aggregate(Max('bid'))
        highestBid = highestBid.get('bid__max')
        if highestBid is None:
            highestBid = listing.startBid
        if bid <= highestBid:
            messages.error(request, 'Bid must be higher than current bid')
        else:
            newBid = Bid.objects.create(bid=bid, bidUser=request.user)
            listing.bids.add(newBid)
            listing.save()
            messages.success(request, 'Bid placed')
    else:
        if not allBids:
            currentPrice = listing.startBid
        else:
            currentPrice = allBids.all().aggregate(Max('bid'))
            currentPrice = currentPrice.get('bid__max')
    return render(request, 'auctions/listing.html', {
        "listing": listing,
        "currentPrice": currentPrice,
        "interested": listing.interested.all(),
        "comments": listing.comments.all()
    })


@login_required
def addwatchlist(request, id):
        listing = Listing.objects.get(pk=id)
        if request.user in listing.interested.all():
            listing.interested.remove(request.user)
        else:
            listing.interested.add(request.user)
        return HttpResponseRedirect(reverse("listing", args=(id,)))

def closeListing(request, id):
    listing = Listing.objects.get(pk=id)
    listing.active = False
    listing.save()

    allBids = listing.bids.all()
    currentPrice = allBids.all().aggregate(Max('bid'))
    currentPrice = currentPrice.get('bid__max')

    winnerObj = allBids.get(bid=currentPrice)
    winner = winnerObj.bidUser
    listing.winner = winner
    listing.save()
    return HttpResponseRedirect(reverse("listing", args=(id,)))

def comment(request, id):
    listing = Listing.objects.get(pk=id)
    comment = request.POST['comment']
    commentObj = Comment.objects.create(comment=comment)
    listing.comments.add(commentObj)
    listing.save()
    messages.success(request, 'Comment posted!')
    return HttpResponseRedirect(reverse("listing", args=(id,)))

def watchlist(request, id):
    user = User.objects.get(pk=id)
    watchlist = user.watchlist.all()
    return render(request, 'auctions/watchlist.html', {
        "listings": watchlist
    })

def categories(request):
    categories = Listing.objects.values_list('category', flat=True)
    categories = list(set(categories))


