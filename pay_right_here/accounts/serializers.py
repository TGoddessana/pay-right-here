from rest_framework import serializers
from pay_right_here.accounts.models import User


class RegisterSerializer(serializers.ModelSerializer):
    """회원가입을 처리하는 serializer 입니다."""

    class Meta:
        model = User
        fields = ["password", "email", "name"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        """회원가입 시 비밀번호를 암호화하여 저장합니다."""
        user = super(RegisterSerializer, self).create(validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return user


class WithdrawSerializer(serializers.ModelSerializer):
    pass
