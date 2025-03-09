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
    queryset = Borrowing.objects.select_related("book", "user")
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self) -> type(serializers.ModelSerializer):
        if self.action == "list":
            return BorrowingListSerializer
        if self.action == "retrieve":
            return BorrowingRetrieveSerializer
        return BorrowingSerializer

    def get_queryset(self) -> QuerySet:
        queryset = self.queryset

        user_id = self.request.query_params.get("user_id", None)
        is_active = self.request.query_params.get("is_active", None)

        if is_active is not None:
            is_active = is_active.lower() in ("true", "t", "1")

        if is_active:
            queryset = queryset.filter(actual_return_date__isnull=True)
        elif is_active is False:
            queryset = queryset.filter(actual_return_date__isnull=False)

        if self.request.user.is_staff:
            if user_id:
                queryset = queryset.filter(user_id=user_id)
        else:
            queryset = queryset.filter(user=self.request.user)

        return queryset
