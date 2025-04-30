from rest_framework.serializers import ModelSerializer
from .models import Recipe
from users.serializer import PublicUserSerializer


class SeeRecipeSerializer(ModelSerializer):
    user = PublicUserSerializer(read_only=True)

    class Meta:
        model = Recipe
        exclude = (
            "video_link",
            "description",
        )


class DetailDetailRecipeSerializer(ModelSerializer):
    user = PublicUserSerializer(read_only=True)


class DetailRecipeSerializer(ModelSerializer):
    class Meta:
        model = Recipe
        field = "__all__"
