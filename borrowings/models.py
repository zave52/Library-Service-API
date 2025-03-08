from datetime import date

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models


class Borrowing(models.Model):
    borrow_date = models.DateField(auto_now_add=True)
    expected_return_date = models.DateField()
    actual_return_date = models.DateField(blank=True, null=True)
    book = models.ForeignKey(
        "Book",
        on_delete=models.CASCADE,
        related_name="borrowings"
    )
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="borrowings"
    )

    @staticmethod
    def validate_borrowing_dates(
        borrow_date: date,
        expected_return_date: date,
        actual_return_date: date,
        error_to_raise: type(Exception)
    ) -> None:
        if expected_return_date and expected_return_date < borrow_date:
            raise error_to_raise(
                {
                    "expected_return_date": "Expected return date "
                                            "must be after the borrow date."
                }
            )

        if actual_return_date and actual_return_date < borrow_date:
            raise error_to_raise(
                {
                    "actual_return_date": "Actual return date "
                                          "must be after the borrow date."
                }
            )

    def clean(self) -> None:
        Borrowing.validate_borrowing_dates(
            self.borrow_date,
            self.expected_return_date,
            self.actual_return_date,
            ValidationError
        )

    def __str__(self) -> str:
        return (
            f"{self.user.email} borrowed {self.book.title} "
            f"on {self.borrow_date}"
        )
