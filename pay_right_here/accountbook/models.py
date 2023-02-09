import uuid

from django.db import models
from pay_right_here.accounts.models import User


class TimestampedModel(models.Model):
    """모델의 생성일자와 수정일자를 저장합니다. abstract=True 이므로 실제 데이터베이스에는 테이블이 생기지 않습니다."""

    class Meta:
        abstract = True

    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)


class AccountBook(TimestampedModel):
    """
    가계부 모델입니다.
    각각의 필드는 아래의 의미를 가집니다.

    - user : 가계부 작성자
    - title : 가계부 제목
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=20)

    def __str__(self):
        return f"<{self.title} | {self.user.name}>"


class AccountBookHistory(TimestampedModel):
    """
    작성내역 모델입니다.
    각각의 필드는 아래의 의미를 가집니다.

    - accountbook : 가계부
    - memo : 메모
    - amount : 금액, - 값일 경우 소비를, + 값일 경우 생산을 의미
    """

    accountbook = models.ForeignKey(AccountBook, on_delete=models.CASCADE)
    memo = models.CharField(max_length=150)
    amount = models.BigIntegerField()

    def __str__(self):
        return f"<{self.memo} | {self.amount}>"


class CopiedAccountBookHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    accountbook_history = models.JSONField(default=dict)

    def __str__(self):
        return f"<{self.user}, 복제된 작성내역 {self.id}>"
