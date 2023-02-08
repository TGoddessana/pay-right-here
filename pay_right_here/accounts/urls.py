from django.urls import path
from pay_right_here.accounts import views

urlpatterns = [
    path("register/", views.RegisterView.as_view(), name="register-account"),
]
