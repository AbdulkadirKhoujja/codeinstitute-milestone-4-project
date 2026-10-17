"""Validate configuration before Django can serve a request."""

import os
import re
from dataclasses import dataclass, field
from collections.abc import Mapping

from django.core.exceptions import ImproperlyConfigured


@dataclass(frozen=True)
class Environment:
    name: str
    debug: bool
    secret_key: str = field(repr=False)
    allowed_hosts: list[str]


def load_environment(values: Mapping[str, str] | None = None) -> Environment:
    values = os.environ if values is None else values
    name = values.get("DJANGO_ENV", "production")
    if name not in {"development", "production"}:
        raise ImproperlyConfigured("DJANGO_ENV must be development or production.")

    debug_value = values.get("DJANGO_DEBUG", "true" if name == "development" else "false")
    if debug_value.lower() not in {"true", "false", "1", "0"}:
        raise ImproperlyConfigured("DJANGO_DEBUG must be true, false, 1, or 0.")
    debug = debug_value.lower() in {"true", "1"}
    if name == "production" and debug:
        raise ImproperlyConfigured("DJANGO_DEBUG must be false in production.")

    secret = values.get("DJANGO_SECRET_KEY", "")
    if (
        len(secret) < 50
        or len(set(secret)) < 5
        or secret.startswith(("django-insecure-", "replace-me-"))
    ):
        raise ImproperlyConfigured("DJANGO_SECRET_KEY must be a strong, non-placeholder key of at least 50 characters.")

    default_hosts = "localhost,127.0.0.1,[::1]" if name == "development" else ""
    hosts = [host.strip() for host in values.get("DJANGO_ALLOWED_HOSTS", default_hosts).split(",")]
    host_pattern = r"(?=.{1,253}$)(?:[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?)(?:\.[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?)*"
    if not hosts or any(host != "[::1]" and not re.fullmatch(host_pattern, host) for host in hosts):
        raise ImproperlyConfigured("DJANGO_ALLOWED_HOSTS must contain explicit hostnames without schemes, ports, or wildcards.")

    return Environment(name=name, debug=debug, secret_key=secret, allowed_hosts=hosts)
