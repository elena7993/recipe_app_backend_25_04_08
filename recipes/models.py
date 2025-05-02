from django.db import models
from common.models import CommonModel


class Recipe(CommonModel):
    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
    )

    title = models.CharField(
        max_length=50,
    )

    description = models.TextField()

    img = models.URLField(
        null=True,
        blank=True,
    )

    video_link = models.CharField(
        max_length=200,
        null=True,
        blank=True,
    )

    like = models.ManyToManyField(
        "users.User",
        blank=True,
        related_name="recipes",
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "레시피👀"
