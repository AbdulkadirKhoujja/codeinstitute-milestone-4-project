from django.shortcuts import render

def home(request):
    """Public foundation page; no workshop functionality is implemented yet."""
    return render(request, "core/home.html")
