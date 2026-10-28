from django.urls import path

from . import views

urlpatterns = [
    path("", views.entry, name="household_entry"),
    path("create/", views.create, name="household_create"),
    path("<int:household_id>/settings/", views.settings, name="household_settings"),
    path("invitations/<str:token>/", views.invitation, name="household_invitation"),
    path("join/<str:flow>/", views.join, name="household_join"),
]
