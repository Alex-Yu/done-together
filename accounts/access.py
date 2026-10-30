from functools import wraps

from allauth.account.models import EmailAddress
from django.http import HttpResponseForbidden


def verified_parent_required(view):
    @wraps(view)
    def guarded(request, *args, **kwargs):
        if (
            not request.user.is_authenticated
            or not EmailAddress.objects.filter(
                user=request.user, email__iexact=request.user.email, verified=True
            ).exists()
        ):
            return HttpResponseForbidden("A verified parent account is required.")
        return view(request, *args, **kwargs)

    return guarded
