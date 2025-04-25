from django.urls import path
from . import views

urlpatterns = [
    path("", views.SeeRecipes.as_view()),
]
