from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError

from pay_right_here.accounts.models import User


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label="비밀번호", widget=forms.PasswordInput)
    password2 = forms.CharField(label="비밀번호 확인", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ("email", "name")
        labels = {"email": "이메일", "name": "이름"}

    def clean_password2(self):
        """회원가입 시, 사용자가 입력한 비밀번호 필드 두 개가 일치하는지 확인합니다."""
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("비밀번호가 일치하지 않습니다.")
        return password2

    def save(self, commit=True):
        """입력받은 비밀번호를 암호화하여 사용자를 저장합니다."""
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """사용자 정보 수정 폼을 정의합니다."""

    readonly_fields = "password"
    password = ReadOnlyPasswordHashField(label="비밀번호")

    class Meta:
        model = User
        fields = ("email", "password", "name", "is_admin")
        labels = {
            "email": "이메일",
            "name": "이름",
            "is_admin": "관리자 여부",
        }


class UserAdmin(BaseUserAdmin):
    """사용자 어드민 클래스를 정의합니다."""

    form = UserChangeForm
    add_form = UserCreationForm
    list_display = ("email", "name", "is_admin")
    list_filter = ("is_admin",)
    fieldsets = (
        ("계정 정보", {"fields": ("name", "email", "password")}),
        ("관리자 여부", {"fields": ("is_admin",)}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "name", "password1", "password2"),
            },
        ),
    )
    search_fields = ("email",)
    ordering = ("email",)
    filter_horizontal = ()


admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
