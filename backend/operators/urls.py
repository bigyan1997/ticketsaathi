from django.urls import path
from .views import ApplyOperatorView, OperatorProfileView, OperatorDetailView

urlpatterns = [
    path('apply/',         ApplyOperatorView.as_view(),   name='operator-apply'),
    path('profile/',       OperatorProfileView.as_view(), name='operator-profile'),
    path('<slug:slug>/',   OperatorDetailView.as_view(),  name='operator-detail'),
]
