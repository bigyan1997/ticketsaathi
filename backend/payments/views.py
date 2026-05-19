from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import PermissionDenied, NotFound
from django.utils import timezone
from .models import Payment
from .serializers import PaymentSerializer, PaymentCreateSerializer, PaymentConfirmSerializer
from bookings.models import Booking


class PaymentCreateView(generics.CreateAPIView):
    """
    POST /api/payments/
    Initiates a payment for a booking.
    The frontend then redirects the user to eSewa or Khalti to complete payment.
    """

    serializer_class = PaymentCreateSerializer
    permission_classes = (permissions.IsAuthenticated,)


class PaymentConfirmView(APIView):
    """
    POST /api/payments/{id}/confirm/
    Called after the user completes payment on eSewa/Khalti.
    The frontend sends back the transaction_id from the payment gateway.
    This marks the payment as completed and confirms the booking.
    """

    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, pk):
        try:
            payment = Payment.objects.get(pk=pk)
        except Payment.DoesNotExist:
            raise NotFound('Payment not found.')

        # Only the booking owner can confirm their own payment
        if payment.booking.user != request.user:
            raise PermissionDenied('You do not have permission to confirm this payment.')

        if payment.status == 'completed':
            return Response({'detail': 'Payment already confirmed.'}, status=status.HTTP_200_OK)

        serializer = PaymentConfirmSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Mark payment as completed
        payment.transaction_id = serializer.validated_data['transaction_id']
        payment.status = 'completed'
        payment.paid_at = timezone.now()
        payment.save(update_fields=['transaction_id', 'status', 'paid_at'])

        # Mark the booking as confirmed
        booking = payment.booking
        booking.status = 'confirmed'
        booking.save(update_fields=['status'])

        return Response(PaymentSerializer(payment).data, status=status.HTTP_200_OK)


class PaymentDetailView(generics.RetrieveAPIView):
    """GET /api/payments/{id}/ — view details of one payment (owner only)."""

    serializer_class = PaymentSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        try:
            payment = Payment.objects.get(pk=self.kwargs['pk'])
        except Payment.DoesNotExist:
            raise NotFound('Payment not found.')

        if payment.booking.user != self.request.user:
            raise PermissionDenied('You do not have permission to view this payment.')

        return payment
