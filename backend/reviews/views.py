from rest_framework import generics, permissions
from rest_framework.exceptions import PermissionDenied
from .models import Review
from .serializers import ReviewSerializer, ReviewCreateSerializer


class ReviewListView(generics.ListAPIView):
    """
    GET /api/reviews/?trip={id}
    Public list of reviews. Pass ?trip=5 to see reviews for a specific trip.
    """

    serializer_class = ReviewSerializer
    permission_classes = (permissions.AllowAny,)

    def get_queryset(self):
        qs = Review.objects.all()
        trip_id = self.request.query_params.get('trip')
        if trip_id:
            qs = qs.filter(trip_id=trip_id)
        return qs


class ReviewCreateView(generics.CreateAPIView):
    """POST /api/reviews/ — leave a review for a trip you completed."""

    serializer_class = ReviewCreateSerializer
    permission_classes = (permissions.IsAuthenticated,)


class ReviewDeleteView(generics.DestroyAPIView):
    """DELETE /api/reviews/{id}/ — delete your own review."""

    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        try:
            review = Review.objects.get(pk=self.kwargs['pk'])
        except Review.DoesNotExist:
            raise PermissionDenied('Review not found.')

        if review.user != self.request.user:
            raise PermissionDenied('You can only delete your own reviews.')

        return review
