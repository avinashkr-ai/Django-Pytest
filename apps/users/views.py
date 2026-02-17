from rest_framework import generics, permissions

from .serializers import UserRegistrationSerializer


class UserRegistrationView(generics.CreateAPIView):
    """
    Simple user registration endpoint.
    """

    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]

