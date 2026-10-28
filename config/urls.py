from django.urls import path

from board import views

urlpatterns = [
    path("", views.landing, name="landing"),
    path("health/", views.health, name="health"),
    path("smoke/", views.smoke, name="smoke"),
]
