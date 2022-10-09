from django.urls import path
from .views import (
    UsersListView,
    UserView,
    UserCreateView,
    LoginView,
    LogoutView,
    VerifyOTPView,
    UserDetailView,
)

urlpatterns = [
    path('users/', UsersListView.as_view(), name='users'),
    path('users/<int:pk>/', UserView.as_view(), name='user'),
    path('users/create/', UserCreateView.as_view(), name='user-create'),
    path('users/login/', LoginView.as_view(), name='user-login'),
    path('users/verify/', VerifyOTPView.as_view(), name='user-verify'),
    path('users/logout/', LogoutView.as_view(), name='user-logout'),
    path('users/detail/', UserDetailView.as_view(), name='user-detail'),
]