from rest_framework_simplejwt.tokens import AccessToken as OriginalAccessToken
from rest_framework_simplejwt.tokens import BlacklistMixin


class AccessToken(OriginalAccessToken, BlacklistMixin):
    """로그아웃을 위해서 토큰 클래스를 재정의합니다."""
