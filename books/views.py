from rest_framework import viewsets

from books.models import Book
from books.permissions import IsAdminOrReadOnly
from books.serializers import BookSerializer


class BookViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing book resources.
    """
    serializer_class = BookSerializer
    queryset = Book.objects.all()
    permission_classes = (IsAdminOrReadOnly,)

    def list(self, request, *args, **kwargs):
        """
        List all books.

        Lists all available books in the database.
        This action is available to all users.
        """
        return super().list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        """
        Create a new book.

        Creates a new book entry with the provided data.
        This action is restricted to admin users only.
        """
        return super().create(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve a specific book.

        Fetches and returns details of a specific book by its ID.
        This action is available to all users.
        """
        return super().retrieve(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        """
        Update a book completely.

        Updates all fields of a specific book.
        This action is restricted to admin users only.
        """
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        """
        Update a book partially.

        Updates only specified fields of a specific book.
        This action is restricted to admin users only.
        """
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """
        Delete a book.

        Removes a specific book from the database.
        This action is restricted to admin users only.
        """
        return super().destroy(request, *args, **kwargs)
