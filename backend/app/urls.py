from django.urls import path

from . import views

urlpatterns = [
    path("", views.sample_data, name="sample_data"),
]