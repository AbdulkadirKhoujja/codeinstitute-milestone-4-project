"""Root routing for the SkillSeat foundation."""

from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("accounts.urls")),
    path("workshops/", include("workshops.urls")),
    path("", include("core.urls")),
]
