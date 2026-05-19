from django.urls import path
from .views import PaymentCreateView, PaymentConfirmView, PaymentDetailView

urlpatterns = [
    path('',              PaymentCreateView.as_view(),  name='payment-create'),
    path('<int:pk>/',     PaymentDetailView.as_view(),  name='payment-detail'),
    path('<int:pk>/confirm/', PaymentConfirmView.as_view(), name='payment-confirm'),
]
