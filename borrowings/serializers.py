from django.utils import timezone
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from books.models import Book
from books.serializers import BookSerializer
from borrowings.models import Borrowing


class BorrowingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        fields = ("id", "expected_return_date", "book")

    def validate_book(self, book: Book) -> Book:
        if book.inventory < 1:
            raise serializers.ValidationError(
                "This book is not available - inventory is 0."
            )
        return book

    def validate(self, attrs: dict) -> dict:
        borrow_date = timezone.now().date()
        expected_return_date = attrs.get("expected_return_date")
        actual_return_date = attrs.get("actual_return_date")

        Borrowing.validate_borrowing_dates(
            borrow_date=borrow_date,
            expected_return_date=expected_return_date,
            actual_return_date=actual_return_date,
            error_to_raise=serializers.ValidationError
        )

        return attrs

    def create(self, validated_data: dict) -> Borrowing:
        validated_data["user"] = self.context["request"].user

        book = validated_data["book"]
        book.inventory -= 1
        book.save()

        return super().create(validated_data)


class BorrowingListSerializer(serializers.ModelSerializer):
    book = serializers.SlugRelatedField(
        many=False,
        read_only=True,
        slug_field="title"
    )
    user = serializers.SlugRelatedField(
        many=False,
        read_only=True,
        slug_field="email"
    )

    class Meta:
        model = Borrowing
        fields = (
            "id", "borrow_date", "expected_return_date",
            "actual_return_date", "book", "user"
        )


class BorrowingRetrieveSerializer(BorrowingListSerializer):
    book = BookSerializer(read_only=True, many=False)


class BorrowingReturnSerializer(BorrowingListSerializer):
    class Meta:
        model = Borrowing
        fields = (
            "id", "book", "borrow_date",
            "expected_return_date", "actual_return_date",
        )
        read_only_fields = (
            "id", "book", "borrow_date", "expected_return_date",
            "actual_return_date"
        )

    def validate(self, attrs: dict) -> dict:
        borrowing = self.instance

        if borrowing.actual_return_date is not None:
            raise ValidationError(
                {
                    "error": f"The book {borrowing.book.title} has already been "
                             f"returned on {borrowing.actual_return_date}."
                },
            )

        Borrowing.validate_borrowing_dates(
            borrow_date=borrowing.borrow_date,
            expected_return_date=borrowing.expected_return_date,
            actual_return_date=timezone.now().date(),
            error_to_raise=ValidationError
        )

        return attrs

    def update(self, instance: Borrowing, validated_data: dict) -> Borrowing:
        instance.actual_return_date = validated_data.get(
            "actual_return_date",
            timezone.now().date()
        )
        instance.book.inventory += 1
        instance.book.save(update_fields=["inventory"])
        instance.save(update_fields=["actual_return_date"])

        return instance
