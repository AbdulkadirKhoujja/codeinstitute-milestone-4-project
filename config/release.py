"""Explicit Heroku policy; local foundation defaults remain independent."""

from dataclasses import dataclass, field
from urllib.parse import urlsplit

import dj_database_url
from django.core.exceptions import ImproperlyConfigured


@dataclass(frozen=True)
class Release:
    database: dict | None = field(repr=False)
    proxy_header: tuple | None
    csrf_origins: list[str]
    storage_backend: str


def load_release(values, *, production):
    deployment = values.get("DJANGO_DEPLOYMENT", "local")
    if deployment not in ("local", "heroku"):
        raise ImproperlyConfigured("DJANGO_DEPLOYMENT must be local or heroku.")
    hosted = deployment == "heroku"
    if values.get("DYNO") and not hosted:
        raise ImproperlyConfigured("Heroku dynos require DJANGO_DEPLOYMENT=heroku.")
    if hosted and not production:
        raise ImproperlyConfigured("Heroku requires production environment policy.")
    origins = [
        part.strip()
        for part in values.get("DJANGO_CSRF_TRUSTED_ORIGINS", "").split(",")
        if part.strip()
    ]
    for origin in origins:
        parsed = urlsplit(origin)
        if (
            parsed.scheme != "https"
            or not parsed.hostname
            or parsed.username
            or parsed.password
            or "*" in origin
            or parsed.path
            or parsed.query
            or parsed.fragment
        ):
            raise ImproperlyConfigured(
                "CSRF trusted origins must be explicit HTTPS origins without paths or credentials."
            )
    url = values.get("DATABASE_URL", "")
    database = None
    if url:
        try:
            parsed = urlsplit(url)
            if (
                parsed.scheme not in ("postgres", "postgresql")
                or not parsed.hostname
                or not parsed.path.strip("/")
            ):
                raise ValueError
            database = dj_database_url.parse(
                url, conn_max_age=60, conn_health_checks=True, ssl_require=production
            )
        except (ValueError, TypeError, dj_database_url.UnknownSchemeError):
            raise ImproperlyConfigured(
                "DATABASE_URL must be a valid PostgreSQL connection URL."
            ) from None
        if production:
            database.setdefault("OPTIONS", {})["sslmode"] = "require"
    if hosted and (database is None or not origins):
        raise ImproperlyConfigured(
            "Heroku requires PostgreSQL DATABASE_URL and explicit DJANGO_CSRF_TRUSTED_ORIGINS."
        )
    return Release(
        database,
        ("HTTP_X_FORWARDED_PROTO", "https") if hosted else None,
        origins,
        "database" if hosted else "filesystem",
    )
