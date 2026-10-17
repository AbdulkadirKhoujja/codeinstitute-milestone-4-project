from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import ProfileForm, RegistrationForm


@login_required
def profile(request):
    """Only the authenticated user's own identity is exposed."""
    return render(request, "accounts/profile.html")


def register(request):
    form = RegistrationForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Account created. You can now sign in.")
        return redirect("accounts:login")
    return render(request, "accounts/form.html", {"form": form, "heading": "Create your account"})


@login_required
def edit(request):
    form = ProfileForm(request.POST or None, instance=request.user)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Account updated.")
        return redirect("accounts:profile")
    return render(request, "accounts/form.html", {"form": form, "heading": "Edit your account"})
