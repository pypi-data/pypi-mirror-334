from django.urls import path

from .views import UserView

app_name = "sampleapp"
urlpatterns = [
    path("users/", UserView.as_view(), name="users-list"),
]
