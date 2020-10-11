from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Item(models.Model):
	"""Auction Items"""
	seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sellers")
	title = models.CharField(max_length=64)
	description = models.TextField(max_length=10000)
	starting_bid = models.DecimalField(max_digits=8, decimal_places=2)
	image = models.CharField(max_length=256, blank=True)
	active = models.BooleanField(default=True)
	date_listed = models.DateTimeField(auto_now=True)

	def __str__(self):
		return f"{self.title}"


class Bids(models.Model):
	bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bidders")
	item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name="items")
	value = models.DecimalField(max_digits=8, decimal_places=2)
	dateTime = models.DateTimeField(auto_now=True)

	def __str__(self):
		return f"{self.value}"

class Watchlist(models.Model):
	watcher = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watchers")
	item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name="watching")
