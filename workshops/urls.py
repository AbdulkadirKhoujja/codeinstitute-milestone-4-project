from django.urls import path

from . import views

app_name = "workshops"
urlpatterns = [
    path("resources/<int:pk>/", views.download, name="download"),
    path("resources/<int:pk>/delete/", views.delete_resource, name="delete_resource"),
    path("reviews/<int:pk>/delete/", views.delete_review, name="delete_review"),
    path("<int:pk>/review/", views.review, name="review"),
    path("studio/<int:pk>/resources/", views.upload_resource, name="upload_resource"),
    path("studio/bookings/<int:pk>/attend/", views.attend, name="attend"),
    path("studio/", views.studio, name="studio"),
    path("studio/new/", views.edit_workshop, name="create"),
    path("studio/<int:pk>/", views.edit_workshop, name="edit"),
    path("bookings/", views.bookings, name="bookings"),
    path("bookings/<int:pk>/cancel/", views.cancel, name="cancel"),
    path("<int:pk>/book/", views.book, name="book"),
    path("", views.listing, name="list"),
    path("<int:pk>/", views.detail, name="detail"),
]
