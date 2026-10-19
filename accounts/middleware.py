"""Database-shared limits; keys retain no plaintext username or address."""

import ipaddress
import math
from datetime import timedelta

from django.conf import settings
from django.db import DatabaseError
from django.db.models import F
from django.shortcuts import render
from django.utils import timezone
from django.utils.crypto import salted_hmac

from .models import AuthThrottle


class AuthenticationThrottleMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.method != "POST" or request.path not in (
            "/accounts/login/",
            "/accounts/register/",
            "/admin/login/",
        ):
            return self.get_response(request)
        address = request.META.get("REMOTE_ADDR", "unknown")
        if settings.SECURE_PROXY_SSL_HEADER and request.headers.get("X-Forwarded-For"):
            candidate = request.headers["X-Forwarded-For"].split(",")[-1].strip()
            try:
                address = str(ipaddress.ip_address(candidate))
            except ValueError:
                pass
        username = request.POST.get("username", "").strip().casefold()
        registration = request.path == "/accounts/register/"
        scopes = (
            [(f"register:{address}", 10)]
            if registration
            else [(f"login:{address}:{username}", 5), (f"network:{address}", 30)]
        )
        now = timezone.now()
        keys = [
            (salted_hmac("skillseat-auth", scope, algorithm="sha256").hexdigest(), limit)
            for scope, limit in scopes
        ]
        try:
            for key, limit in keys:
                bucket = AuthThrottle.objects.filter(
                    pk=key, expires_at__gt=now, failures__gte=limit
                ).first()
                if bucket:
                    response = render(request, "429.html", status=429)
                    response["Retry-After"] = str(
                        max(1, math.ceil((bucket.expires_at - now).total_seconds()))
                    )
                    response["Cache-Control"] = "no-store"
                    return response
        except DatabaseError:
            return render(request, "500.html", status=503)
        response = self.get_response(request)
        # CSRF/method denials are not credential attempts. Registration counts successes too.
        if response.status_code == 200 or (registration and response.status_code == 302):
            try:
                for key, _ in keys:
                    deadline = (
                        now + timedelta(hours=1) if registration else now + timedelta(minutes=15)
                    )
                    AuthThrottle.objects.get_or_create(key=key, defaults={"expires_at": deadline})
                    AuthThrottle.objects.filter(pk=key, expires_at__lte=now).update(
                        failures=0, expires_at=deadline
                    )
                    AuthThrottle.objects.filter(pk=key).update(failures=F("failures") + 1)
            except DatabaseError:
                return render(request, "500.html", status=503)
        return response
