from django.urls import path
from rest_framework_simplejwt.views import TokenBlacklistView

from pay_right_here.accountbook import views


urlpatterns = [
    path("", views.AccountBookListAPIView.as_view(), name="AccountBook-list"),
    path(
        "<int:pk>/", views.AccountBookDetailAPIView.as_view(), name="AccountBook-detail"
    ),
    path(
        "<int:pk>/histories/",
        views.AccountBookHistoryListAPIView.as_view(),
        name="AccountBookHistory-list",
    ),
    path(
        "<int:pk>/histories/<int:history_pk>/",
        views.AccountBookHistoryDetailAPIView.as_view(),
        name="AccountBookHistory-detail",
    ),
]
