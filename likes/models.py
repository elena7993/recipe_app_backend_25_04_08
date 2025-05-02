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
        related_name="likes",
        # 이름을 보기쉽게 바꿀 수 있음
    )

    class Meta:
        verbose_name_plural = "좋아요❣️"
