from django.db.models import QuerySet
from rest_framework import viewsets, mixins, serializers

from borrowings.models import Borrowing
from borrowings.serializers import (
    BorrowingListSerializer,
    BorrowingRetrieveSerializer
)


class BorrowingViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
    queryset = Borrowing.objects.all()

    def get_serializer_class(self) -> type(serializers.ModelSerializer):
        if self.action == "list":
            return BorrowingListSerializer
        return BorrowingRetrieveSerializer

    def get_queryset(self) -> QuerySet:
        queryset = self.queryset
        if self.action == "retrieve":
            queryset = queryset.select_related("book")

        return queryset
