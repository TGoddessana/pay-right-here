import json
from django.urls import reverse
from rest_framework.test import APITestCase
from django.test import Client
from rest_framework_simplejwt.tokens import RefreshToken

from pay_right_here.accountbook.models import AccountBook, AccountBookHistory
from pay_right_here.accounts.models import User, UserManager


class AccountBookListTest(APITestCase):
    """가계부 생성, 조회에 대해서 테스트합니다."""

    def setUp(self):
        """테스트를 위해서 사용자 두 명, 가계부 3개를 생성합니다."""

        # 기본 URL 정의
        self.url = reverse("AccountBook-list")

        # 사용자 두 명 철수와 금수 생성
        self.client = Client(enforce_csrf_checks=True)
        self.chulsu = User.objects.create_user(
            email="example1@example.com", name="철수", password="1234"
        )
        self.geumsu = User.objects.create_user(
            email="example2@example.com", name="금수", password="1234"
        )

        # 철수가 가계부 두 개, 금수가 가계부 한 개 생성
        self.chulsu_accountbook_1 = AccountBook.objects.create(
            user=self.chulsu, title="철수의 가계부 1"
        )
        self.chulsu_accountbook_2 = AccountBook.objects.create(
            user=self.chulsu, title="철수의 가계부 2"
        )
        self.geumsu_accountbook_2 = AccountBook.objects.create(
            user=self.geumsu, title="금수의 가계부 1"
        )

    def test_chulsuJWTRequest_should_count_2(self):
        """철수의 JWT 와 함께 가계부 목록 조회 요청을 보내면, 금수의 가계부는 보이지 않아야 하고 철수가 작성한 가계부 두 개만 보여야 합니다."""

        # 데이터베이스에는 총 3개의 가계부가 존재합니다.
        self.assertEqual(3, AccountBook.objects.count())
        # 철수의 JWT와 함께 가계부 목록 조회 요청을 보냅니다.
        access_token = str(RefreshToken.for_user(self.chulsu).access_token)
        response = self.client.get(
            f"{self.url}", HTTP_AUTHORIZATION="Bearer {}".format(access_token)
        )
        # 철수가 작성한 가계부 2개만 조회됩니다.
        self.assertEqual(2, len(response.data))

    def test_geumsuJWTRequest_should_success_with_userGeumsu(self):
        """
        금수의 JWT와 함께 가계부 생성 요청을 보내면, 금수의 가계부가 생성되어야 합니다.
        """
        access_token = str(RefreshToken.for_user(self.geumsu).access_token)
        register_data = {
            "title": "금수의 가계부 2",
        }
        response = self.client.post(
            f"{self.url}",
            json.dumps(register_data),
            HTTP_AUTHORIZATION="Bearer {}".format(access_token),
            content_type="application/json",
        )
        # 알맞는 데이터와 URL 로 수행되어진 요청은 성공해야 합니다.
        self.assertEqual(response.status_code, 201)
        # 알맞는 데이터와 URL 로 수행되어진 요청이 상태 코드 201 로 성공했다면, 데이터베이스에 존재하는 가계부의 갯수는 4개여야 합니다.
        self.assertEqual(4, AccountBook.objects.count())
        # 마지막에 생성된 가계부의 저자는 금수여야 합니다.
        self.assertEqual("금수", AccountBook.objects.latest("id").user.name)


class AccountBookDetailTest(APITestCase):
    """가계부 생성, 조회, 삭제에 대해서 테스트합니다."""

    def setUp(self):
        """테스트를 위해서 사용자 두 명, 가계부 3개를 생성합니다."""

        # 사용자 두 명 철수와 금수 생성
        self.client = Client(enforce_csrf_checks=True)
        self.chulsu = User.objects.create_user(
            email="example1@example.com", name="철수", password="1234"
        )
        self.geumsu = User.objects.create_user(
            email="example2@example.com", name="금수", password="1234"
        )

        # 철수가 가계부 두 개, 금수가 가계부 한 개 생성
        self.chulsu_accountbook_1 = AccountBook.objects.create(
            user=self.chulsu, title="철수의 가계부 1"
        )
        self.chulsu_accountbook_2 = AccountBook.objects.create(
            user=self.chulsu, title="철수의 가계부 2"
        )
        self.geumsu_accountbook_1 = AccountBook.objects.create(
            user=self.geumsu, title="금수의 가계부 1"  # 이 가계부는 데이터베이스에서 id 가 3 으로 저장
        )

    def test_geumsuJWTRetrieveRequest_should_success(self):
        """금수의 JWT와 함께 가계부 상세조회 요청을 보내면, 금수의 가계부가 조회되어야 합니다."""

        # 금수가 작성한 가계부 리소스를 나타내는 URL 정의
        self.url = reverse("AccountBook-detail", kwargs={"pk": 3})
        access_token = str(RefreshToken.for_user(self.geumsu).access_token)
        response = self.client.get(
            f"{self.url}",
            HTTP_AUTHORIZATION="Bearer {}".format(access_token),
        )
        # 알맞는 데이터와 URL 로 수행되어진 요청은 성공해야 합니다.
        self.assertEqual(response.status_code, 200)
        # 요청이 성공했다면 조회가 잘 되었는지 테스트합니다.
        self.assertEqual(response.data.get("title"), "금수의 가계부 1")

    def test_chulsuJWTRetrieveRequest_should_fail(self):
        """철수의 JWT와 함께 가계부 상세조회 요청을 보내면, 요청이 실패해야 합니다."""

        # 금수가 작성한 가계부 리소스를 나타내는 URL 정의
        self.url = reverse("AccountBook-detail", kwargs={"pk": 3})
        access_token = str(RefreshToken.for_user(self.chulsu).access_token)
        response = self.client.get(
            f"{self.url}",
            HTTP_AUTHORIZATION="Bearer {}".format(access_token),
        )
        # 철수의 인증 정보와 URL 로 수행되어진 요청은 실패해야 합니다.
        self.assertEqual(response.status_code, 404)

    def test_geumsuJWTPutRequest_should_success(self):
        """금수의 JWT와 함께 가계부 수정 요청을 보내면, 금수의 가계부가 잘 수정되어야 합니다."""

        # 금수가 작성한 가계부 리소스를 나타내는 URL 정의
        self.url = reverse("AccountBook-detail", kwargs={"pk": 3})
        access_token = str(RefreshToken.for_user(self.geumsu).access_token)
        update_data = {"title": "수정된 금수의 가계부 1"}
        response = self.client.put(
            f"{self.url}",
            json.dumps(update_data),
            HTTP_AUTHORIZATION="Bearer {}".format(access_token),
            content_type="application/json",
        )
        # 알맞는 데이터와 URL 로 수행되어진 요청은 성공해야 합니다.
        self.assertEqual(response.status_code, 200)

        # 요청이 성공했다면 조회가 잘 되었는지 테스트합니다.
        self.assertEqual(response.data.get("title"), "수정된 금수의 가계부 1")

    def test_chulsuJWTPutRequest_should_fail(self):
        """철수의 JWT와 함께 가계부 수정 요청을 보내면, 철수의 가계부가 아니므로 찾을 수 없고 요청이 실패해야 합니다."""

        # 금수가 작성한 가계부 리소스를 나타내는 URL 정의
        self.url = reverse("AccountBook-detail", kwargs={"pk": 3})
        access_token = str(RefreshToken.for_user(self.chulsu).access_token)
        update_data = {"title": "수정된 금수의 가계부 1"}
        response = self.client.put(
            f"{self.url}",
            json.dumps(update_data),
            HTTP_AUTHORIZATION="Bearer {}".format(access_token),
            content_type="application/json",
        )
        # 철수의 인증 정보와 금수의 가계부 상세 URL 로 수행되어진 요청은 실패해야 합니다.
        self.assertEqual(response.status_code, 404)

    def test_geumsuJWTDeleteRequest_should_success(self):
        """금수의 JWT와 함께 가계부 삭제 요청을 보내면, 금수의 가계부가 삭제되어야 합니다."""

        # 금수가 작성한 가계부 리소스를 나타내는 URL 정의
        self.url = reverse("AccountBook-detail", kwargs={"pk": 3})
        access_token = str(RefreshToken.for_user(self.geumsu).access_token)
        response = self.client.delete(
            f"{self.url}",
            HTTP_AUTHORIZATION="Bearer {}".format(access_token),
            content_type="application/json",
        )
        # 알맞는 데이터와 URL 로 수행되어진 요청은 성공해야 합니다.
        self.assertEqual(response.status_code, 204)

        # 삭제 요청이 성공했으면, 맨 처음에 생성한 가계부 개수 3개에서 2개로 잘 변경되었는지 확인합니다.
        self.assertEqual(2, AccountBook.objects.count())


class AccountBookHistoryListTest(APITestCase):
    """가계부 작성목록의 목록조회, 생성에 대해 테스트합니다."""

    def setUp(self):
        """테스트를 위해서 사용자 두 명, 가계부 3개를 생성합니다."""

        # 사용자 두 명 철수와 금수 생성
        self.client = Client(enforce_csrf_checks=True)
        self.chulsu = User.objects.create_user(
            email="example1@example.com", name="철수", password="1234"
        )
        self.geumsu = User.objects.create_user(
            email="example2@example.com", name="금수", password="1234"
        )

        # 철수와 금수의 가계부 각각 하나씩 생성
        self.chulsu_accountbook_1 = AccountBook.objects.create(
            user=self.chulsu, title="철수의 가계부 1"
        )
        self.geumsu_accountbook_1 = AccountBook.objects.create(
            user=self.geumsu, title="금수의 가계부 1"
        )

        # 철수의 가계부 1 에 철수의 작성내역 2개 생성
        self.chulsu_accounbookhistory_1 = AccountBookHistory.objects.create(
            accountbook=self.chulsu_accountbook_1, memo="철수가 아이스크림을 사먹음", amount=-1000
        )
        self.chulsu_accounbookhistory_2 = AccountBookHistory.objects.create(
            accountbook=self.chulsu_accountbook_1, memo="철수가 용돈을 받음", amount=5000
        )

    def test_chulsuJWTListRequest_should_success(self):
        """철수의 JWT 로 철수의 작성내역 조회 요청을 하면, 성공해야 하고 결과는 2개여야 합니다."""
        # 철수 작성한 가계부 리소스(철수의 가계부 1) 를 나타내는 URL 정의
        self.url = reverse("AccountBookHistory-list", kwargs={"pk": 1})
        access_token = str(RefreshToken.for_user(self.chulsu).access_token)
        response = self.client.get(
            f"{self.url}",
            HTTP_AUTHORIZATION="Bearer {}".format(access_token),
            content_type="application/json",
        )
        # 알맞는 데이터와 URL 로 수행되어진 요청은 성공해야 합니다.
        self.assertEqual(response.status_code, 200)
        # 그리고 해당 요청의 결과의 갯수는 2개여야 합니다.
        self.assertEqual(2, len(response.data))

    def test_geumsuJWTListRequest_should_fail(self):
        """금수의 JWT 로 철수의 작성내역 조회 요청을 하면, 실패해야 합니다."""
        # 철수 작성한 가계부 리소스(철수의 가계부 1) 를 나타내는 URL 정의
        self.url = reverse("AccountBookHistory-list", kwargs={"pk": 1})
        access_token = str(RefreshToken.for_user(self.geumsu).access_token)
        response = self.client.get(
            f"{self.url}",
            HTTP_AUTHORIZATION="Bearer {}".format(access_token),
            content_type="application/json",
        )
        # 금수의 인증 정보와 URL 로 수행되어진 요청은 실패해야 합니다.
        self.assertEqual(response.status_code, 403)

    def test_chulsuJWTListCreateRequest_should_success(self):
        """철수의 JWT 로 철수의 작성내역 생성 요청을 하면, 성공해야 하고 생성 후 결과는 3개여야 합니다."""
        # 철수 작성한 가계부 리소스(철수의 가계부 1) 를 나타내는 URL 정의
        self.url = reverse("AccountBookHistory-list", kwargs={"pk": 1})
        access_token = str(RefreshToken.for_user(self.chulsu).access_token)
        update_data = {
            "memo": "철수가 피자를 사먹음",
            "amount": 19000,
            "accountbook": self.chulsu_accountbook_1.id,
        }
        response = self.client.post(
            f"{self.url}",
            json.dumps(update_data),
            HTTP_AUTHORIZATION="Bearer {}".format(access_token),
            content_type="application/json",
        )
        # 알맞는 데이터와 URL 로 수행되어진 요청은 성공해야 합니다.
        self.assertEqual(response.status_code, 201)
        # 그리고 작성내역이 성공적으로 생성되었다면 모든 작성내역의 갯수는 최종적으로 3개여야 합니다.
        self.assertEqual(3, AccountBookHistory.objects.count())

    def test_geumsuJWTListCreateRequest_should_success(self):
        """금수의 JWT 로 철수의 가계부에 작성내역 생성 요청을 하면, 실패해야 합니다."""
        # 철수 작성한 가계부 리소스(철수의 가계부 1) 를 나타내는 URL 정의
        self.url = reverse("AccountBookHistory-list", kwargs={"pk": 1})
        access_token = str(RefreshToken.for_user(self.geumsu).access_token)
        update_data = {
            "memo": "금수가 피자를 사먹음",
            "amount": 19000,
            "accountbook": self.chulsu_accountbook_1.id,
        }
        response = self.client.post(
            f"{self.url}",
            json.dumps(update_data),
            HTTP_AUTHORIZATION="Bearer {}".format(access_token),
            content_type="application/json",
        )
        # 금수의 인증 정보와 URL 로 수행되어진 요청은 실패해야 합니다.
        self.assertEqual(response.status_code, 403)
