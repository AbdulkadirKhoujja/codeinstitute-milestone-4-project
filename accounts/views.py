from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def profile(request):
    """Only the authenticated user's own identity is exposed."""
    return render(request, "accounts/profile.html")
