from django.db import transaction
from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse
from rest_framework import viewsets, mixins, serializers, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from borrowings.models import Borrowing
from borrowings.serializers import (
    BorrowingListSerializer,
    BorrowingRetrieveSerializer,
    BorrowingSerializer,
    BorrowingReturnSerializer
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
        if self.action == "borrowing_return":
            return BorrowingReturnSerializer
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

    @action(
        methods=["POST"],
        detail=True,
        permission_classes=(IsAuthenticated,),
        url_path="return"
    )
    def borrowing_return(
        self, request: HttpRequest, pk: int, *args, **kwargs
    ) -> HttpResponse:
        borrowing = self.get_object()

        serializer = self.get_serializer(
            borrowing,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)

        with transaction.atomic():
            serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)
