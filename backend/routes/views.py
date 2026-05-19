from rest_framework import generics, permissions
from rest_framework.exceptions import PermissionDenied
from .models import Route, Bus, Trip
from .serializers import (
    RouteSerializer, RouteCreateSerializer,
    BusSerializer,
    TripSerializer, TripCreateSerializer,
)


class IsOperator(permissions.BasePermission):
    """Only allow users who have an operator profile."""

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_operator)


# ── Routes ────────────────────────────────────────────────────────────────────

class RouteListView(generics.ListAPIView):
    """GET /api/routes/ — anyone can browse all active routes."""

    serializer_class = RouteSerializer
    permission_classes = (permissions.AllowAny,)
    queryset = Route.objects.filter(is_active=True)


class RouteDetailView(generics.RetrieveAPIView):
    """GET /api/routes/{slug}/ — public detail of one route."""

    serializer_class = RouteSerializer
    permission_classes = (permissions.AllowAny,)
    queryset = Route.objects.all()
    lookup_field = 'slug'


class RouteCreateView(generics.CreateAPIView):
    """POST /api/routes/create/ — operators only."""

    serializer_class = RouteCreateSerializer
    permission_classes = (IsOperator,)


# ── Buses ─────────────────────────────────────────────────────────────────────

class BusListCreateView(generics.ListCreateAPIView):
    """
    GET  /api/routes/buses/ — list the logged-in operator's own buses
    POST /api/routes/buses/ — add a new bus
    """

    serializer_class = BusSerializer
    permission_classes = (IsOperator,)

    def get_queryset(self):
        # Operators can only see their own buses
        return Bus.objects.filter(operator=self.request.user.operator_profile)


# ── Trips ─────────────────────────────────────────────────────────────────────

class TripListView(generics.ListAPIView):
    """
    GET /api/routes/trips/ — public trip search.
    Optional query params: ?origin=Kathmandu&destination=Pokhara&date=2026-05-20
    """

    serializer_class = TripSerializer
    permission_classes = (permissions.AllowAny,)

    def get_queryset(self):
        qs = Trip.objects.filter(status='scheduled', available_seats__gt=0)

        origin = self.request.query_params.get('origin')
        destination = self.request.query_params.get('destination')
        date = self.request.query_params.get('date')  # format: YYYY-MM-DD

        if origin:
            qs = qs.filter(route__origin__icontains=origin)
        if destination:
            qs = qs.filter(route__destination__icontains=destination)
        if date:
            qs = qs.filter(departure_time__date=date)

        return qs


class TripDetailView(generics.RetrieveAPIView):
    """GET /api/routes/trips/{slug}/ — view details of one trip."""

    serializer_class = TripSerializer
    permission_classes = (permissions.AllowAny,)
    queryset = Trip.objects.all()
    lookup_field = 'slug'


class TripCreateView(generics.CreateAPIView):
    """POST /api/routes/trips/ — operators only."""

    serializer_class = TripCreateSerializer
    permission_classes = (IsOperator,)
