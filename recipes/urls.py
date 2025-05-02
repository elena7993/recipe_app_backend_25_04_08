from django.urls import path
from . import views

urlpatterns = [
    path("", views.SeeRecipes.as_view()),
    path("<int:pk>", views.RecipeDetail.as_view()),
    path("<int:pk>/like", views.RecipeLike.as_view()),
    path("<int:pk>/comments", views.SeeComment.as_view()),
]
