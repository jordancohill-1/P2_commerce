from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms
import re  
from django.forms import ModelForm, Textarea, ModelChoiceField
from .models import User, Item, Bids, Watchlist, Comments, Categories, ItemInCategory
from django.db.models import Max
from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import login_required

class NewItemForm(ModelForm):
    class Meta:
        model = Item
        fields = ['title', 'description', 'starting_bid', 'image', 'category']
        category = ModelChoiceField(queryset=Categories.objects.all())
       
class NewCommentForm(ModelForm):
    class Meta:
        model = Comments
        fields = ['comment']

#helpers
def currentUser(request):
    return User.objects.get(id = request.user.id)

def getItem(id):
    return Item.objects.get(pk = id) 

def getHighestBid(Item):
    #return Bids.objects.filter(item = Item).aggregate(Max('value')).get(value__max)
    return Bids.objects.filter(item = Item).order_by('value').last()

#


def index(request):

    return render(request, "auctions/index.html",{
        "items": Item.objects.filter(active = True).all(),
        })

def watching(request):
    return render(request, "auctions/watching.html",{
        "items": Watchlist.objects.filter(watcher = currentUser(request)).all()
        })
def category(request):
    return render(request, "auctions/category.html",{
        "categories": Categories.objects.all()
        })

def category_results(request, name):
    c = Categories.objects.filter(name = name).get()
    return render(request, "auctions/category_results.html",{
        "items": Item.objects.filter(category = c.id).all(),
        "name" : name
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
    if request.method == "POST":
        form = NewItemForm(request.POST)
        if(form.is_valid()):
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            starting_bid = form.cleaned_data['starting_bid']
            image = form.cleaned_data['image']
            category = form.cleaned_data['category']
            item = Item(seller = currentUser(request), title = title, description = description, starting_bid =starting_bid, image = image, category = category)#get id from session not url
            item.save();

            return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/create.html",  {
                "form": NewItemForm,
                "categories": Categories.objects.all()
            })

def item(request, item_id):
    item = getItem(item_id)
    disable = not item.active
    comments = Comments.objects.filter(item = item).all()
    print(disable)
    if request.user.is_authenticated:
        user = currentUser(request)
        on_watchlist = Watchlist.objects.filter(watcher = user.id, item = item_id).exists();
        is_creator =(item.active == True)&(user.id == getItem(item_id).seller.id)
        if(getHighestBid(item)):
            winner = (user.id == (getHighestBid(item)).bidder.id)
        else:
            winner = None

    
    else:
        on_watchlist = None
        is_creator = None 

    return render(request, "auctions/item.html",  {
                "item":item,
                "on_watchlist":on_watchlist,
                "currentBid": getHighestBid(item),
                "is_creator": is_creator,
                "winner": winner,
                "form": NewCommentForm,
                "comments": comments,
                "disable" : disable

            })

@login_required
def watchlist(request, item_id, on_watchlist):
    if request.method == "POST":
        if(on_watchlist == "True"):
                w = Watchlist.objects.get(watcher = request.user.id, item = item_id)
                w.delete();
        else:
            w = Watchlist(watcher = currentUser(request), item = getItem(item_id))
            w.save();    
    return HttpResponseRedirect(reverse("item", args=(str(item_id))))

@login_required
def bid(request, item_id):
    if request.method == "POST":
        newBid = float(request.POST["value"])
        starting_bid = getItem(item_id).starting_bid
        bid = Bids(bidder =  currentUser(request), item = getItem(item_id), value = newBid)
        if(getHighestBid(getItem(item_id))):
            currBid = (getHighestBid(getItem(item_id))).value
            if(newBid > currBid):
                bid.save()
            else:
                return HttpResponse("Your bid must be greater than the current bid.")
        elif(newBid >= starting_bid):
            bid.save()
        else:
            return HttpResponse("Your bid must be equal to or greater than the starting bid.")

    return HttpResponseRedirect(reverse("item", args=(str(item_id)))) 

@login_required
def close(request, item_id):
    if request.method == "POST":
        item = getItem(item_id)
        item.active = False;
        item.save()

    return HttpResponseRedirect(reverse("item", args=(str(item_id)))) 

@login_required
def comment(request, item_id):
    if request.method == "POST":
        form = NewCommentForm(request.POST)
        if(form.is_valid()):
            comment = form.cleaned_data['comment']
            c = Comments(commenter = currentUser(request), item = getItem(item_id), comment = comment)
            c.save()

    return HttpResponseRedirect(reverse("item", args=(str(item_id))))




