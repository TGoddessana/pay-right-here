from django.urls import path, include
from rest_framework.routers import SimpleRouter
from pay_right_here.accountbook import views

router = SimpleRouter()
router.register("", views.AccountBookViewSet, basename="AccountBook")

urlpatterns = [
    path("", include(router.urls)),
]
