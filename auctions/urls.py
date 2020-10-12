from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("item/<int:item_id>", views.item, name="item"),
    path("watchlist/<int:item_id>/<str:on_watchlist>", views.watchlist, name="watchlist"),
    path("bid/<int:item_id>", views.bid, name="bid"),
    path("close/<int:item_id>", views.close, name="close"),
    path("comment/<int:item_id>", views.comment, name="comment" ),
    path("watching", views.watching, name="watching"),
    path("category", views.category, name="category"),
    path("category_results/<str:name>", views.category_results, name="category_results")
]
