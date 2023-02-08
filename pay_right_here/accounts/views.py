from rest_framework import generics, status
from rest_framework.response import Response

from pay_right_here.accounts.models import User
from pay_right_here.accounts.serializers import RegisterSerializer, WithdrawSerializer


class RegisterView(generics.CreateAPIView):
    """회원가입을 처리하는 View 입니다. POST 메서드만 허용됩니다."""

    queryset = User.objects.all()
    serializer_class = RegisterSerializer


class WithdrawView(generics.DestroyAPIView):
    pass
