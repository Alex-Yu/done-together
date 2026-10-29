"""One household lock spans revision and every lazy template query.

All board writers take this same lock before changes; ordinary READ COMMITTED
therefore produces one scoped snapshot without holding a transaction over HTTP.
"""

from django.db import transaction
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.utils import timezone
from django.views.decorators.http import require_GET

from accounts.access import verified_parent_required
from board.read_model import columns_for_household, household_week
from households.models import Household
from households.pin_views import parent_context
from households.services import household_for_parent


@require_GET
@verified_parent_required
@transaction.atomic
def snapshot(request, household_id):
    household_for_parent(request.user, household_id)
    household = Household.objects.select_for_update().get(pk=household_id)
    context = parent_context(request, household)
    key = f"{household.revision}:{household_week(household, timezone.now())[0].isoformat()}:{bool(context['parent_authority'])}"
    payload = {"key": key, "unlocked": bool(context["parent_authority"])}
    if request.GET.get("key") != key:
        context["columns"] = columns_for_household(household)
        payload["columns"] = render_to_string("board/columns.html", context, request)
        payload["schedules"] = render_to_string(
            "board/schedules.html", context, request
        )
    return JsonResponse(payload)
