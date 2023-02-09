from django.shortcuts import redirect
from django.http import HttpResponseNotFound
from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from config.settings.development import REDIS_CLIENT, REDIS_EXPIRATION_TIME
from pay_right_here.accountbook.models import AccountBook, AccountBookHistory
from pay_right_here.accountbook.serializers import (
    AccountBookSerializer,
    AccountBookHistoryListSerializer,
    CopiedAccountBookHistoryListSerializer,
)
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import generics, status

from pay_right_here.accountbook.permissions import AccountBookHistoryPermission
from pay_right_here.accountbook.utils import generate_short_code


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


class AccountBookHistoryDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """가계부 작성내역 상세에 대한 View 입니다."""

    lookup_url_kwarg = "history_pk"
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


class CopiedAccountBookHistoryListView(generics.ListCreateAPIView):
    """가계부 작성내역을 복제하고, 목록 조회를 처리하는 APIView 입니다."""

    serializer_class = CopiedAccountBookHistoryListSerializer

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


@api_view(["GET"])
def shorten_url(request, *args, **kwargs):
    """단축 URL 생성을 처리하는 view 입니다."""
    url = request.GET.get("url", None)
    if not url:
        return Response(
            {"error": "No URL provided"}, status=status.HTTP_400_BAD_REQUEST
        )
    shortened_url = REDIS_CLIENT.get(url)
    if shortened_url:
        REDIS_CLIENT.expire(url, REDIS_EXPIRATION_TIME)
        REDIS_CLIENT.expire(shortened_url.decode("utf-8"), REDIS_EXPIRATION_TIME)
        return Response({"shortened_url": shortened_url.decode("utf-8")})
    short_code = generate_short_code()
    while REDIS_CLIENT.get(short_code):
        short_code = generate_short_code()
    REDIS_CLIENT.set(url, short_code)
    REDIS_CLIENT.expire(url, REDIS_EXPIRATION_TIME)
    REDIS_CLIENT.set(short_code, url)
    REDIS_CLIENT.expire(short_code, REDIS_EXPIRATION_TIME)

    return Response({"shortened_url": short_code})


def short_url_redirect(request, short_code):
    """단축 URL 로 접근 시, 원래의 url로 redirect 시켜주는 view 입니다."""
    original_url = REDIS_CLIENT.get(short_code.encode())
    if original_url:
        original_url = original_url.decode()
        return redirect(original_url)
    else:
        return HttpResponseNotFound("Short URL not found")
