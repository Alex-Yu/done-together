from django.http import JsonResponse
from django.urls import path

from accounts.access import verified_parent_required
from config.urls import urlpatterns as app_patterns


@verified_parent_required
def protected_fixture(request):
    return JsonResponse({"fixture": "verified-account-only"})


urlpatterns = [*app_patterns, path("_test/protected/", protected_fixture)]
