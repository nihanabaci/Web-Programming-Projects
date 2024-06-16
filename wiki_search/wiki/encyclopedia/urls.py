from django.urls import path

from . import views

app_name = "click"
urlpatterns = [
    path("", views.index, name="index"),
    path("newpage", views.newpage, name="newpage"),
    path("wiki/<str:title>", views.entry, name="title"),
    path("search", views.search, name='search'),
    path("random", views.random, name='random'),
    path("edit/<str:editPage>", views.edit, name='editPage')

]
