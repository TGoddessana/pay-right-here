from rest_framework import serializers
from pay_right_here.accountbook.models import (
    AccountBook,
    AccountBookHistory,
    CopiedAccountBookHistory,
)


class AccountBookSerializer(serializers.ModelSerializer):
    """가계부 목록에 대한 직렬화&역직렬화 규칙을 정의합니다."""

    class Meta:
        model = AccountBook
        fields = [
            "id",
            "title",
        ]
        extra_kwargs = {
            "user": {"read_only": True},
        }


class AccountBookHistoryListSerializer(serializers.ModelSerializer):
    """가계부 작성내역 목록에 대한 직렬화/역직렬화 규칙을 정의합니다."""

    class Meta:
        model = AccountBookHistory
        fields = "__all__"


class CopiedAccountBookHistoryListSerializer(serializers.ModelSerializer):
    """복제된 가계부 작성내역 목록에 대한 직렬화/역직렬화 규칙을 정의합니다."""

    class Meta:
        model = CopiedAccountBookHistory
        fields = "__all__"
