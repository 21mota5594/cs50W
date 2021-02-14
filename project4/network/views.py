from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
import json

from .models import User, Post, UserFollowing


def index(request):
    posts = Post.objects.all().order_by('-timestamp')
    paginator = Paginator(posts, 5)

    pageNum = request.GET.get('page')
    page_obj = paginator.get_page(pageNum)

    user = User.objects.get(username='joss')
    followers = user.followers.all()
    return render(request, "network/index.html", {
        "page_obj": page_obj
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
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


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
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password) 
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

@login_required
def post(request):
    # Composing new post must be via POST
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    data = json.loads(request.body)
    post = data.get("post")
    if post == [""]:
        return JsonResponse({"error": "At least one recipient required."}, status=400)

    post = Post(post=post, poster=request.user, likes=0)
    post.save()

    return JsonResponse({"message": "Post published successfully."}, status=201)

@login_required
def profile(request, username):
    try:
        profileUser = User.objects.get(username=username)
    except User.DoesNotExist:
        messages.error(request, "Profile does not exist.")
        return HttpResponseRedirect(reverse("index"))
    userPosts = Post.objects.filter(poster=profileUser).order_by('-timestamp')
    paginator = Paginator(userPosts, 5)

    pageNum = request.GET.get('page')
    page_obj = paginator.get_page(pageNum)

    followers = profileUser.followers.all()
    followersList = []
    for follower in followers:
        followersList.append(follower.userId)
    return render(request, "network/profile.html", {
        "profileUser": profileUser,
        "profileFollowers": followersList,
        "followersNum": len(followers),
        "followingNum": len(profileUser.following.all()),
        "page_obj": page_obj
    })


@login_required
@csrf_exempt
def follow(request, username):
    if request.method == "PUT":
        data = json.loads(request.body)
        followAction = data.get("followAction")
        reqUser = request.user
        otherUser = User.objects.get(username=username)
        if followAction == "follow":
            # add reqUser to otherUser's followers
            followObj = UserFollowing.objects.create(userId=reqUser, followingUserId=otherUser)
            followObj.save()
        else:
            unfollowObj = UserFollowing.objects.get(userId=reqUser, followingUserId=otherUser)
            unfollowObj.delete()
        return JsonResponse({"message": "Follow action complete"}, status=201)
    else:
        return JsonResponse({"error": "PUT request required"}, status=400)


@login_required
def edit(request):
    if request.method != "PUT":
        return JsonResponse({"error": "PUT request required"}, status=400)
    
    data = json.loads(request.body)
    oldText = data.get("oldText")
    newText = data.get("newText")

    try:
        post = Post.objects.get(post=oldText)
    except Post.DoesNotExist:
        messages.error(request, "Post does not exist.")
        return HttpResponseRedirect(reverse("index"))
    
    if request.user != post.poster:
        return JsonResponse({"error": "User missing required authentication."})
    post.post = newText
    post.save()

    return JsonResponse({"success": "Post edited succesfully."})

        