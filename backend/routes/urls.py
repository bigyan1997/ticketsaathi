from django.urls import path
from .views import (
    RouteListView, RouteDetailView, RouteCreateView,
    BusListCreateView,
    TripListView, TripDetailView, TripCreateView,
)

urlpatterns = [
    # Routes
    path('',                    RouteListView.as_view(),   name='route-list'),
    path('create/',             RouteCreateView.as_view(), name='route-create'),
    path('<slug:slug>/',        RouteDetailView.as_view(), name='route-detail'),

    # Buses
    path('buses/', BusListCreateView.as_view(), name='bus-list-create'),

    # Trips
    path('trips/',              TripListView.as_view(),   name='trip-list'),
    path('trips/create/',       TripCreateView.as_view(), name='trip-create'),
    path('trips/<slug:slug>/',  TripDetailView.as_view(), name='trip-detail'),
]
