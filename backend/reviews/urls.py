from django.urls import path
from .views import ReviewListView, ReviewCreateView, ReviewDeleteView

urlpatterns = [
    path('',           ReviewListView.as_view(),   name='review-list'),
    path('create/',    ReviewCreateView.as_view(),  name='review-create'),
    path('<int:pk>/',  ReviewDeleteView.as_view(),  name='review-delete'),
]
