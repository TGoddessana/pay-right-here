from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser


class UserManager(BaseUserManager):
    """새로운 사용자를 생성하기 위한 UserManager 를 정의합니다."""

    def create_user(self, email, name, password=None):
        if not name:
            raise ValueError("이름이 필요합니다.")
        if not email:
            raise ValueError("이메일 주소가 필요합니다.")
        user = self.model(email=self.normalize_email(email), name=name)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password=None):
        user = self.create_user(email=email, name=name, password=password)
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    """
    사용자 모델입니다.
    email, name, password, is_admin 필드를 가집니다.
    """

    email = models.EmailField(
        max_length=255,
        unique=True,
    )
    name = models.CharField(max_length=30, blank=False)
    is_admin = models.BooleanField(default=False)
    objects = UserManager()
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name"]

    @property
    def is_staff(self):
        return self.is_admin

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    def __str__(self):
        return f"<{self.name} | {self.email}>"
