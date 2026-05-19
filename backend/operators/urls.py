from django.urls import path
from .views import ApplyOperatorView, OperatorProfileView

urlpatterns = [
    path('apply/',   ApplyOperatorView.as_view(),   name='operator-apply'),
    path('profile/', OperatorProfileView.as_view(), name='operator-profile'),
]
