from django.urls import include, path

from board import views

urlpatterns = [
    path("accounts/", include("accounts.urls")),
    path("", views.landing, name="landing"),
    path("health/", views.health, name="health"),
    path("smoke/", views.smoke, name="smoke"),
]
