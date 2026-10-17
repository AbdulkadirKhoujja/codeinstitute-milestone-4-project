from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.urls import path, reverse_lazy

from . import views

app_name = "accounts"
urlpatterns = [
    path("register/", views.register, name="register"),
    path("edit/", views.edit, name="edit"),
    path(
        "password/",
        PasswordChangeView.as_view(
            template_name="accounts/form.html",
            success_url=reverse_lazy("accounts:profile"),
            extra_context={"heading": "Change your password"},
        ),
        name="password",
    ),
    path("", views.profile, name="profile"),
    path("login/", LoginView.as_view(template_name="accounts/login.html"), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
]
