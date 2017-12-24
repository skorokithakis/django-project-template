"""The main application's URLs."""

from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name="index"),
]  # yapf: disable
