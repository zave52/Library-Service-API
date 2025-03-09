from django.db.models import QuerySet
from rest_framework import viewsets, mixins, serializers
from rest_framework.permissions import IsAuthenticated

from borrowings.models import Borrowing
from borrowings.serializers import (
    BorrowingListSerializer,
    BorrowingRetrieveSerializer,
    BorrowingSerializer
)


class BorrowingViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet
):
    queryset = Borrowing.objects.all()
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self) -> type(serializers.ModelSerializer):
        if self.action == "list":
            return BorrowingListSerializer
        if self.action == "retrieve":
            return BorrowingRetrieveSerializer
        return BorrowingSerializer

    def get_queryset(self) -> QuerySet:
        queryset = self.queryset
        if self.action == "retrieve":
            queryset = queryset.select_related("book")

        return queryset
