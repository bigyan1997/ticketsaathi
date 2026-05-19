from rest_framework import generics, permissions
from rest_framework.exceptions import PermissionDenied
from .models import Booking
from .serializers import BookingSerializer, BookingCreateSerializer


class BookingListView(generics.ListAPIView):
    """GET /api/bookings/ — a passenger sees only their own bookings."""

    serializer_class = BookingSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user)


class BookingCreateView(generics.CreateAPIView):
    """POST /api/bookings/ — create a new booking."""

    serializer_class = BookingCreateSerializer
    permission_classes = (permissions.IsAuthenticated,)


class BookingDetailView(generics.RetrieveAPIView):
    """GET /api/bookings/{id}/ — view details of one booking (owner only)."""

    serializer_class = BookingSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        try:
            booking = Booking.objects.get(pk=self.kwargs['pk'])
        except Booking.DoesNotExist:
            raise PermissionDenied('Booking not found.')

        # Passengers can only see their own bookings
        if booking.user != self.request.user:
            raise PermissionDenied('You do not have permission to view this booking.')

        return booking


class BookingCancelView(generics.UpdateAPIView):
    """
    PATCH /api/bookings/{id}/cancel/ — cancel a booking.
    Sets status to 'cancelled' and frees up the seat.
    """

    serializer_class = BookingSerializer
    permission_classes = (permissions.IsAuthenticated,)
    http_method_names = ['patch']

    def get_object(self):
        try:
            booking = Booking.objects.get(pk=self.kwargs['pk'])
        except Booking.DoesNotExist:
            raise PermissionDenied('Booking not found.')

        if booking.user != self.request.user:
            raise PermissionDenied('You do not have permission to cancel this booking.')

        if booking.status == 'cancelled':
            raise PermissionDenied('This booking is already cancelled.')

        return booking

    def perform_update(self, serializer):
        booking = self.get_object()
        booking.status = 'cancelled'
        booking.save(update_fields=['status'])

        # Free up the seat back on the trip
        trip = booking.trip
        trip.available_seats += 1
        trip.save(update_fields=['available_seats'])
