from django.db import DatabaseError, connection
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_GET, require_POST


@require_GET
@never_cache
def health(request):
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            cursor.fetchone()
    except DatabaseError:
        return JsonResponse({"status": "unavailable"}, status=503)
    return JsonResponse({"status": "ok"})


@require_GET
@never_cache
def landing(request):
    if request.user.is_authenticated:
        from allauth.account.models import EmailAddress

        from households.models import Membership

        try:
            if EmailAddress.objects.filter(
                user=request.user, email__iexact=request.user.email, verified=True
            ).exists():
                membership = Membership.objects.filter(user=request.user).first()
                if membership:
                    return redirect(
                        "household_board", household_id=membership.household_id
                    )
        except DatabaseError:
            return render(request, "accounts/unavailable.html", status=503)
    return render(request, "landing.html")


@require_POST
@never_cache
def smoke(request):
    return render(request, "smoke.html")
