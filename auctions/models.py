from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Categories(models.Model):
	#lookup
	name = models.CharField(max_length=64)

	def __str__(self):
		return f"{self.name}"

class Item(models.Model):
	"""Auction Items"""
	seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sellers")
	title = models.CharField(max_length=64)
	description = models.TextField(max_length=10000)
	starting_bid = models.DecimalField(max_digits=8, decimal_places=2)
	image = models.CharField(max_length=256, blank=True)
	category = models.ForeignKey(Categories, null=True, on_delete=models.CASCADE,  related_name="categories")
	active = models.BooleanField(default=True)
	date_listed = models.DateTimeField(auto_now=True)

	def __str__(self):
		return f"{self.title}"

	def current_price(self):
		curPrice = max([bid.value for bid in self.item_bids.all()] + [self.starting_bid])
		return curPrice



class Bids(models.Model):
	bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bidders")
	item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name="item_bids")
	value = models.DecimalField(max_digits=8, decimal_places=2)
	dateTime = models.DateTimeField(auto_now=True)

	def __str__(self):
		return f"{self.value}"

class Watchlist(models.Model):
	watcher = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watchers")
	item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name="watching")

	def __str__(self):
		return f"{self.item}"

class Comments(models.Model):
	commenter = models.ForeignKey(User, on_delete=models.CASCADE, related_name="commenters")
	item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name="item_comments")
	comment = models.TextField(max_length=10000)


	def __str__(self):
		return f"{self.comment}"



class ItemInCategory(models.Model):
	category = models.ForeignKey(Categories, on_delete=models.CASCADE, related_name="item_categories")
	item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name="item_category")

	def __init__(self):
		return f"{self.category}"
		
		
		