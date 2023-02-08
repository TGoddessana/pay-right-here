from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from pay_right_here.jwtauth.jwt import AccessToken


@api_view(("POST",))
def jwtauth_logout(request):
    """access token을 Blacklist 에 추가합니다."""
    access_token = AccessToken(token=request.headers.get("Authorization").split(" ")[1])
    access_token.blacklist()
    return Response(status=status.HTTP_204_NO_CONTENT)
