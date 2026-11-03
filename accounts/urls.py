from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    CustomLoginView,
    CurrentUserProfileView,
    ChangePasswordView,
    LogoutView,
)

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='auth-login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('logout/', LogoutView.as_view(), name='auth-logout'),
    path('me/', CurrentUserProfileView.as_view(), name='current-user-profile'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
]