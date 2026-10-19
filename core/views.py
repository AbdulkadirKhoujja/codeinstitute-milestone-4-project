from django.db import DatabaseError, connection
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_safe


def home(request):
    """Public introduction and workshop discovery entry point."""
    return render(request, "core/home.html")


@require_safe
def health(request):
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            cursor.fetchone()
    except DatabaseError:
        response = JsonResponse({"status": "unavailable"}, status=503)
    else:
        response = JsonResponse({"status": "ok"})
    response["Cache-Control"] = "no-store"
    return response


def csrf_failure(request, reason=""):
    return render(request, "403.html", status=403)
