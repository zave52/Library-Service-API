from rest_framework import serializers

from books.serializers import BookSerializer
from borrowings.models import Borrowing


class BorrowingListSerializer(serializers.ModelSerializer):
    book = serializers.SlugRelatedField(
        read_only=True,
        slug_field="title"
    )

    class Meta:
        model = Borrowing
        fields = (
            "id", "borrow_date", "expected_return_date",
            "actual_return_date", "book"
        )


class BorrowingRetrieveSerializer(BorrowingListSerializer):
    book = BookSerializer(read_only=True, many=False)
