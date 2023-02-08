from pay_right_here.accountbook.models import AccountBook
from pay_right_here.accountbook.serializers import AccountBookListSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import generics


class AccountBookListAPIView(generics.ListCreateAPIView):
    serializer_class = AccountBookListSerializer

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
