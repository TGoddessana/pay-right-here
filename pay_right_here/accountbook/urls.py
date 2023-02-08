from django.urls import path
from pay_right_here.accountbook import views


urlpatterns = [
    path("", views.AccountBookListAPIView.as_view(), name="AccountBook-list"),
    path(
        "<int:pk>/", views.AccountBookDetailAPIView.as_view(), name="AccountBook-detail"
    ),
]
