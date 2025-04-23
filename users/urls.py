from django.urls import path, include
from . import views

urlpatterns = [
    path("me/", views.Me.as_view()),
    path("signup/", views.Signup.as_view()),
]
