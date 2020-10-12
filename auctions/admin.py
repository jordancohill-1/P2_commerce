from django.contrib import admin

# Register your models here.
from .models import User, Item, Bids, Watchlist, Comments, Categories, ItemInCategory

admin.site.register(User)
admin.site.register(Item)
admin.site.register(Bids)
admin.site.register(Watchlist)
admin.site.register(Comments)
admin.site.register(Categories)
admin.site.register(ItemInCategory)


