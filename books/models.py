from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import UniqueConstraint
from django.utils.translation import gettext as _


class Book(models.Model):
    class CoverChoices(models.TextChoices):
        HARD = "HARD", _("Hard")
        SOFT = "SOFT", _("Soft")

    title = models.CharField(max_length=255)
    author = models.CharField(max_length=150)
    cover = models.CharField(
        max_length=4,
        choices=CoverChoices,
        default=CoverChoices.SOFT
    )
    inventory = models.PositiveIntegerField()
    daily_fee = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=(MinValueValidator(0),)
    )

    class Meta:
        constraints = (
            UniqueConstraint(
                fields=("title", "author"),
                name="unique_title_author"
            ),
        )

    def __str__(self) -> str:
        return self.title
