from django.contrib.auth import get_user_model
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from users.serializers import UserSerializer


class CreateUserView(generics.CreateAPIView):
    """
    Create a new user in the system.

    This endpoint allows registration of new users with email,
    password, first_name and last_name.
    """
    serializer_class = UserSerializer
    permission_classes = ()


class ManageUserView(generics.RetrieveUpdateAPIView):
    """
    Retrieve or update the authenticated user's information.

    This endpoint allows users to view their own profile details
    or update their information including password, email, first_name,
    and last_name.
    """
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self) -> get_user_model():
        return self.request.user

    def get(self, request, *args, **kwargs):
        """
        Retrieve the authenticated user's information.

        This method handles GET requests and returns the serialized data
        for the currently authenticated user.
        """
        return super().get(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        """
        Update all fields of the authenticated user.

        This method handles PUT requests and performs a complete update
        of the user's information. All required fields must be included
        in the request.
        """
        return super().put(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        """
        Partially update the authenticated user's information.

        This method handles PATCH requests and allows updating only
        specific fields of the user's information. Only the fields
        that need to be modified should be included in the request.
        """
        return super().patch(request, *args, **kwargs)
