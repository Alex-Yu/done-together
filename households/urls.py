from django.urls import path

from board.sync import snapshot
from chores import views as chore_views

from . import pin_views, views

urlpatterns = [
    path("<int:household_id>/snapshot/", snapshot, name="board_snapshot"),
    path(
        "<int:household_id>/chores/<int:occurrence_id>/submit/",
        chore_views.submit,
        name="chore_submit",
    ),
    path(
        "<int:household_id>/chores/<int:occurrence_id>/review/",
        chore_views.review,
        name="chore_review",
    ),
    path(
        "<int:household_id>/recurring/new/",
        chore_views.recurring,
        name="recurring_create",
    ),
    path(
        "<int:household_id>/recurring/<int:definition_id>/edit/",
        chore_views.recurring,
        name="recurring_edit",
    ),
    path(
        "<int:household_id>/recurring/<int:definition_id>/delete/",
        chore_views.recurring,
        {"delete": True},
        name="recurring_delete",
    ),
    path("<int:household_id>/chores/new/", chore_views.manage, name="chore_create"),
    path(
        "<int:household_id>/chores/<int:occurrence_id>/edit/",
        chore_views.manage,
        name="chore_edit",
    ),
    path(
        "<int:household_id>/chores/<int:occurrence_id>/delete/",
        chore_views.manage,
        {"delete": True},
        name="chore_delete",
    ),
    path("<int:household_id>/board/", pin_views.board, name="household_board"),
    path("<int:household_id>/unlock/", pin_views.unlock, name="parent_unlock"),
    path("<int:household_id>/lock/", pin_views.lock, name="parent_lock"),
    path("<int:household_id>/parent-pin/", pin_views.parent_pin, name="parent_pin"),
    path(
        "<int:household_id>/parent-activity/",
        pin_views.activity,
        name="parent_activity",
    ),
    path(
        "<int:household_id>/children/new/", pin_views.child_create, name="child_create"
    ),
    path(
        "<int:household_id>/children/<int:child_id>/edit/",
        pin_views.child_edit,
        name="child_edit",
    ),
    path(
        "<int:household_id>/children/<int:child_id>/pin/",
        pin_views.child_edit,
        {"pin": True},
        name="child_pin",
    ),
    path("", views.entry, name="household_entry"),
    path("create/", views.create, name="household_create"),
    path("<int:household_id>/settings/", views.settings, name="household_settings"),
    path("invitations/<str:token>/", views.invitation, name="household_invitation"),
    path("join/<str:flow>/", views.join, name="household_join"),
]
