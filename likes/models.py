from django.db import models
from common.models import CommonModel


class Like(CommonModel):
    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
    )

    recipe = models.ForeignKey(
        "recipes.Recipe",
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name_plural = "좋아요❣️"
