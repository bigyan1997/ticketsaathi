from rest_framework import generics, permissions
from django.contrib.auth import get_user_model
from .serializers import RegisterSerializer, UserProfileSerializer

User = get_user_model()


class RegisterView(generics.CreateAPIView):
    """POST /api/auth/register/ — create a new user account."""

    serializer_class = RegisterSerializer
    permission_classes = (permissions.AllowAny,)  # no login required to register


class ProfileView(generics.RetrieveUpdateAPIView):
    """GET /api/auth/profile/  — view your profile.
       PUT /api/auth/profile/  — update your profile."""

    serializer_class = UserProfileSerializer
    permission_classes = (permissions.IsAuthenticated,)  # must be logged in

    def get_object(self):
        # Always return the currently logged-in user
        return self.request.user
