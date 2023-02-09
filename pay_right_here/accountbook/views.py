from rest_framework.generics import get_object_or_404
from pay_right_here.accountbook.models import AccountBook, AccountBookHistory
from pay_right_here.accountbook.serializers import (
    AccountBookSerializer,
    AccountBookHistoryListSerializer,
)
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import generics

from pay_right_here.accountbook.permissions import AccountBookHistoryPermission


class AccountBookListAPIView(generics.ListCreateAPIView):
    """가계부 리소스 목록에 대한 View 입니다."""

    serializer_class = AccountBookSerializer

    def get_queryset(self):
        user_id = JWTAuthentication().authenticate(request=self.request)[0].id
        return AccountBook.objects.filter(user_id=user_id)

    def perform_create(self, serializer):
        """현재 로그인한 유저의 id 를 가계부의 저자로 저장"""
        serializer.save(user=self.request.user)
        return super().perform_create(serializer)

    def get_serializer_context(self):
        """serializer 에 추가 context 제공"""
        context = super().get_serializer_context()
        context["request"] = self.request
        return


class AccountBookDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """가계부 리소스 상세에 대한 View 입니다."""

    serializer_class = AccountBookSerializer

    def get_queryset(self):
        user_id = JWTAuthentication().authenticate(request=self.request)[0].id
        return AccountBook.objects.filter(user_id=user_id)


class AccountBookHistoryListAPIView(generics.ListCreateAPIView):
    """가계부 작성내역 목록에 대한 View 입니다."""

    permission_classes = [
        AccountBookHistoryPermission,
    ]
    serializer_class = AccountBookHistoryListSerializer

    def get_queryset(self):
        user_id = JWTAuthentication().authenticate(request=self.request)[0].id
        accountbook_id = self.kwargs.get("pk")
        # 가계부 인스턴스가 존재하지 않으면, 404 Error
        get_object_or_404(AccountBook, id=accountbook_id)

        return AccountBookHistory.objects.filter(accountbook_id=accountbook_id).filter(
            accountbook__user_id=user_id
        )
