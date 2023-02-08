from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from pay_right_here.jwtauth.views import jwtauth_logout

urlpatterns = [
    path("login/", TokenObtainPairView.as_view(), name="jwtauth_login"),
    path("refresh/", TokenRefreshView.as_view(), name="jwtauth_refresh"),
    path("logout/", jwtauth_logout, name="jwtauth_logout"),
]
