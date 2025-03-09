from django.utils import timezone
from rest_framework import serializers

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
