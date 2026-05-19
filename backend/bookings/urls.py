from django.urls import path
from .views import BookingListView, BookingCreateView, BookingDetailView, BookingCancelView

urlpatterns = [
    path('',             BookingListView.as_view(),   name='booking-list'),
    path('create/',      BookingCreateView.as_view(),  name='booking-create'),
    path('<int:pk>/',    BookingDetailView.as_view(),  name='booking-detail'),
    path('<int:pk>/cancel/', BookingCancelView.as_view(), name='booking-cancel'),
]
