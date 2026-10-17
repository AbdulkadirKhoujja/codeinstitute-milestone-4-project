from django.shortcuts import get_object_or_404, render

from .models import Workshop


def listing(request):
    return render(
        request,
        "workshops/list.html",
        {"workshops": Workshop.objects.filter(published=True).select_related("owner")},
    )


def detail(request, pk):
    item = get_object_or_404(Workshop.objects.select_related("owner"), pk=pk, published=True)
    return render(request, "workshops/detail.html", {"workshop": item})
