from rest_framework import generics, permissions
from rest_framework.exceptions import PermissionDenied
from .models import Operator
from .serializers import OperatorSerializer, ApplyOperatorSerializer


class ApplyOperatorView(generics.CreateAPIView):
    """
    POST /api/operators/apply/
    Any logged-in user can apply to become an operator.
    They must not already have an operator profile.
    """

    serializer_class = ApplyOperatorSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def perform_create(self, serializer):
        # Prevent a user from creating a second operator profile
        if Operator.objects.filter(user=self.request.user).exists():
            raise PermissionDenied('You already have an operator profile.')
        serializer.save()


class OperatorProfileView(generics.RetrieveUpdateAPIView):
    """
    GET  /api/operators/profile/  — view your own operator profile
    PUT  /api/operators/profile/  — update your own operator profile
    """

    serializer_class = OperatorSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        try:
            return self.request.user.operator_profile
        except Operator.DoesNotExist:
            raise PermissionDenied('You do not have an operator profile yet.')
