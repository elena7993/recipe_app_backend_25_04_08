from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import Recipe
from users.models import User
from users.serializer import PublicUserSerializer


class LikeSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = (
            "username",
            "avatar",
        )


class SeeRecipeSerializer(ModelSerializer):
    user = PublicUserSerializer(read_only=True)

    class Meta:
        model = Recipe
        exclude = (
            "video_link",
            "description",
        )


class DetailRecipeSerializer(ModelSerializer):
    user = PublicUserSerializer(read_only=True)
    like = LikeSerializer(read_only=True, many=True)
    is_mine = SerializerMethodField()
    is_liked = SerializerMethodField()
    like_count = SerializerMethodField()

    class Meta:
        model = Recipe
        fields = "__all__"

    def get_is_mine(self, recipe):
        req = self.context.get("req")

        if req:
            return recipe.user == req.user
        return False

    def get_is_liked(self, recipe):
        req = self.context.get("req")

        if req:
            return recipe.like.filter(pk=req.user.pk).exists()
        else:
            return False

    def get_like_count(self, recipe):
        req = self.context.get("req")

        if req:
            return recipe.like.count()
