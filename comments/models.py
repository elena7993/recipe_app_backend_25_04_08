from django.db import models
from common.models import CommonModel


class Comments(CommonModel):
    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
    )

    recipe = models.ForeignKey(
        "recipes.Recipe",
        on_delete=models.CASCADE,
        related_name="comments",
    )

    payload = models.TextField()

    rating = models.PositiveIntegerField()

    class Meta:
        verbose_name_plural = "코멘트✔️"
