from rest_framework.serializers import ModelSerializer
from .models import Recipe
from users.serializer import PublicUserSerializer


class SeeRecipeSerializer(ModelSerializer):
    user = PublicUserSerializer(read_only=True)

    class Meta:
        model = Recipe
        fields = "__all__"
