from django.http import JsonResponse
from django.urls import path
from django.views.decorators.http import require_POST

from accounts.access import verified_parent_required
from config.urls import urlpatterns as application_patterns
from households.pins import verify_child_pin


@require_POST
@verified_parent_required
def child_check(request, household_id, child_id):
    return JsonResponse(
        {
            "verified": bool(
                verify_child_pin(
                    request.user, household_id, child_id, request.POST.get("pin", "")
                )
            )
        }
    )


urlpatterns = [
    *application_patterns,
    path(
        "households/<int:household_id>/fixture-child/<int:child_id>/",
        child_check,
        name="fixture_child_check",
    ),
]
