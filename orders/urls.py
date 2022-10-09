from .views import (
    PlaceListCreateAPIView,
    PlaceRetrieveUpdateDestroyAPIView,
    OrderListCreateAPIView,
    OrderRetrieveUpdateDestroyAPIView, 
    OrderHistoryListAPIView,
    OrderListAPIView,
)
from django.urls import path


urlpatterns = [
    path('orders/', OrderListAPIView.as_view(), name='orders'),
    path('orders/create/', OrderListCreateAPIView.as_view(), name='orders'),
    path('orders/<int:pk>/', OrderRetrieveUpdateDestroyAPIView.as_view(), name='order'),
    path('orders/history/', OrderHistoryListAPIView.as_view(), name='order-history'),
    path('places/', PlaceListCreateAPIView.as_view(), name='places'),
    path('places/<int:pk>/', PlaceRetrieveUpdateDestroyAPIView.as_view(), name='place'),
]
