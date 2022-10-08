from django.urls import path
from .views import (
    UsersListView,
    UserView,
    UserCreateView,
    LoginView,
    LogoutView,
)

urlpatterns = [
    path('users/', UsersListView.as_view(), name='users'),
    path('users/<int:pk>/', UserView.as_view(), name='user'),
    path('user/create/', UserCreateView.as_view(), name='user-create'),
    path('user/login/', LoginView.as_view(), name='user-login'),
    path('user/logout/', LogoutView.as_view(), name='user-logout'),
]