from rest_framework import serializers
from .models import Comments
from users.serializer import PublicUserSerializer


class CommentSerializers(serializers.ModelSerializer):
    user = PublicUserSerializer(read_only=True)
    is_mine = serializers.SerializerMethodField()

    class Meta:
        model = Comments
        exclude = ("recipe",)

    def get_is_min(self, comment):
        req = self.context.get("req")

        if req:
            return comment.user == req.user
        else:
            False
