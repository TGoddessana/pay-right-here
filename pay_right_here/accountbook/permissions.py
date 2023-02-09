from rest_framework import permissions
from rest_framework.generics import get_object_or_404

from pay_right_here.accountbook.models import AccountBook, AccountBookHistory


class AccountBookHistoryPermission(permissions.IsAuthenticated):
    """가계부를 다루려면 로그인한 상태에서 다루어야 하고, 본인이 작성한 가계부만 수정하거나, 삭제하거나, 조회할 수 있습니다."""

    def has_permission(self, request, view):
        """
        요청한 사용자의 id가, kwargs로 특정할 수 있는 AccountBook 의 저자의 id와 같은지를 반환합니다.
        작성내역을 생성할 때에는, 자신이 가지고 있는 가계부에만 작성할 수 있어야 합니다.
        """
        # 가계부 인스턴스가 존재하지 않으면, 404 Error
        accountbook_id = view.kwargs.get("pk")
        get_object_or_404(AccountBook, id=accountbook_id)

        accountbook_id_from_client = request.data.get("accountbook")
        if accountbook_id_from_client:
            return (
                request.user.id
                == AccountBook.objects.get(id=accountbook_id_from_client).user.id
                and request.user.id
                == AccountBook.objects.get(id=view.kwargs.get("pk")).user.id
            )
        return (
            request.user.id == AccountBook.objects.get(id=view.kwargs.get("pk")).user.id
        )
