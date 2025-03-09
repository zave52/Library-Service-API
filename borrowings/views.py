from django.db import transaction
from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse
from drf_spectacular.utils import extend_schema, OpenApiParameter
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
    """
    ViewSet for managing borrowing operations.

    Provides functionality to list, retrieve, create borrowings, and return borrowed books.
    """
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

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="is_active",
                description="Filter by active status (not returned). "
                            "Use true/false values (ex. ?is_active=true).",
                required=False,
                type=str,
            ),
            OpenApiParameter(
                name="user_id",
                description="Filter by user ID (staff only) (ex. ?user_id=1).",
                required=False,
                type=int,
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        """
        List all borrowings.

        Regular users can see only their own borrowings.
        Staff users can see all borrowings and filter by user_id.
        Both can filter by active status using is_active parameter.
        """
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve details of a specific borrowing.

        Users can only retrieve their own borrowings unless they are staff.
        """
        return super().retrieve(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        """
        Create a new borrowing.

        The book's inventory will be reduced by 1 upon successful borrowing.
        The user creating the borrowing will automatically be set as the user.
        """
        return super().create(request, *args, **kwargs)

    @action(
        methods=["POST"],
        detail=True,
        permission_classes=(IsAuthenticated,),
        url_path="return"
    )
    def borrowing_return(
        self, request: HttpRequest, pk: int, *args, **kwargs
    ) -> HttpResponse:
        """
        Return a borrowed book.

        Sets actual_return_date to the current date and increases the book's inventory by 1.
        Can only be performed if the book hasn't been returned yet.
        """
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
