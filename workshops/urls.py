from django.urls import path

from . import views

app_name = "workshops"
urlpatterns = [
    path("studio/", views.studio, name="studio"),
    path("studio/new/", views.edit_workshop, name="create"),
    path("studio/<int:pk>/", views.edit_workshop, name="edit"),
    path("bookings/", views.bookings, name="bookings"),
    path("bookings/<int:pk>/cancel/", views.cancel, name="cancel"),
    path("<int:pk>/book/", views.book, name="book"),
    path("", views.listing, name="list"),
    path("<int:pk>/", views.detail, name="detail"),
]
