import json
from django.urls import reverse
from rest_framework.test import APITestCase
from django.test import Client

from pay_right_here.accounts.models import User


class AccountsTests(APITestCase):
    """회원가입, 회원탈퇴에 대해서 테스트합니다."""

    def setUp(self):
        self.client = Client(enforce_csrf_checks=True)

    def test_registerWithValidData_should_success(self):
        """
        정상적인 데이터와 함께 요청을 보냈을 때, 회원가입이 정상적으로 이루어지는지 테스트합니다.
        1. 알맞는 URL 과 데이터로 회원가입 요청을 보내면, 상태 코드는 201이어야 합니다.
        2. 알맞는 URL 과 데이터로 회원가입 요청을 보냈고 상태 코드가 201이라면, 전체 회원의 수는 한 명이어야 합니다.
        """
        self.url = reverse("register-account")
        register_data = {
            "email": "test@test.com",
            "password": "1234",
            "name": "payrighthere",
        }

        response = self.client.post(
            f"{self.url}", json.dumps(register_data), content_type="application/json"
        )
        # 1. 알맞는 URL 과 데이터로 회원가입 요청을 보내면, 상태 코드는 201이어야 합니다.
        self.assertEqual(response.status_code, 201)
        # 2. 알맞는 URL 과 데이터로 회원가입 요청을 보냈고 상태 코드가 201이라면, 전체 회원의 수는 한 명이어야 합니다.
        self.assertEqual(User.objects.all().count(), 1)

    def test_registerWithUnvalidData_should_fail(self):
        """
        유효하지 않은 데이터로 요청을 보냈을 때, 회원가입이 실패하는지 테스트합니다.
        해당 테스트에서는 이메일을 유효하지 않은 데이터로 전송합니다.
        1. 알맞는 URL 과 유효하지 않은 데이터로 회원가입 요청을 보내면, 상태 코드는 400이어야 합니다.
        2. 알맞는 URL 과 유효하지 않은 데이터로 회원가입 요청을 보냈고 상태 코드가 400이라면, 전체 회원의 수는 한 명도 없어야 합니다.
        """
        self.url = reverse("register-account")
        register_data = {
            "email": "testtest.com",  # 이메일 형식과 맞지 않습니다.
            "password": "1234",
            "name": "payrighthere",
        }

        response = self.client.post(
            f"{self.url}", json.dumps(register_data), content_type="application/json"
        )
        # 1. 알맞는 URL 과 유효하지 않은 데이터로 회원가입 요청을 보내면, 상태 코드는 400이어야 합니다.
        self.assertEqual(response.status_code, 400)
        # 2. 알맞는 URL 과 유효하지 않은 데이터로 회원가입 요청을 보냈고 상태 코드가 400이라면, 전체 회원의 수는 한 명도 없어야 합니다.
        self.assertEqual(User.objects.all().count(), 0)
