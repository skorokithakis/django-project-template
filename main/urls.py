"""The main application's URLs."""

from django.urls import path

from . import views

app_name = "main"
urlpatterns = [path("", views.index, name="index")]
