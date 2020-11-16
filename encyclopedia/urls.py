from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("search", views.search, name="search"),
    path("new", views.new_entry, name="new_entry"),
    path("random", views.random, name="random"),
    path("wiki/<str:title>", views.entry, name="entry"),
    path("edit/<str:title>", views.edit_entry, name="edit_entry"),
]
