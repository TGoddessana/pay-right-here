<div align="center">

<h1 align="center">Pay Right Here! - Backend</h1>
  <p align="center">
    소비하고, 기록하고, 찾아보세요. 바로 여기서!
    <br />
    가계부 서비스를 위한 REST API 입니다.
    <br />
    <a href="https://documenter.getpostman.com/view/21924519/2s935smgb8"><strong>REST API 명세서 »</strong></a>
    <br />
    <br />
  </p>
</div>


## About The Project

소비내역을 기록하고, 관리할 수 있는 가계부 서비스를 위한 REST API 입니다.



### Built With

프로젝트에서 사용된 기술 스택을 소개합니다.  
Python 3.11, Django 4.1 환경에서 개발되었습니다.

* [![Python3][Python3]][Python3-url]
* [![Django][Django]][Django-url]
* [![MySQL][MySQL]][MySQL-url]

### Test Cases

프로젝트는 아래의 테스트 케이스를 통과하였습니다.

<details>
<summary>테스트 케이스 상세보기</summary>

### accountbook 앱의 테스트 케이스

```python
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
        """테스트를 위해서 사용자 두 명, 가계부 2개를 생성합니다."""

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

    def test_geumsuJWTListCreateRequest_should_fail(self):
        """금수의 JWT 로 철수의 가계부에 작성내역 생성 요청을 하면, 실패해야 합니다."""
        # 철수 작성한 가계부 리소스(철수의 가계부 1) 를 나타내는 URL 정의
        self.url = reverse("AccountBookHistory-list", kwargs={"pk": 1})
        access_token = str(RefreshToken.for_user(self.geumsu).access_token)
        create_data = {
            "memo": "금수가 피자를 사먹음",
            "amount": 19000,
            "accountbook": self.chulsu_accountbook_1.id,
        }
        response = self.client.post(
            f"{self.url}",
            json.dumps(create_data),
            HTTP_AUTHORIZATION="Bearer {}".format(access_token),
            content_type="application/json",
        )
        # 금수의 인증 정보와 URL 로 수행되어진 요청은 실패해야 합니다.
        self.assertEqual(response.status_code, 403)


class AccountBookHistoryDetailTest(APITestCase):
    """가계부 작성내역의 상세조회, 수정, 삭제에 대해 테스트합니다."""

    def setUp(self):
        """테스트를 위해서 사용자 두 명, 가계부 2개, 각각 가계부에 작성내역 한 개씩을 생성합니다."""

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

        # 각각 가계부에 작성내역 한 개씩 생성
        self.chulsu_accounbookhistory_1 = AccountBookHistory.objects.create(
            accountbook=self.chulsu_accountbook_1, memo="철수가 아이스크림을 사먹음", amount=-1000
        )
        self.geumsu_accountbookhistory_1 = AccountBookHistory.objects.create(
            accountbook=self.geumsu_accountbook_1, memo="금수가 노트북을 삼", amount=-105000
        )

    def test_chulsuJWTDetailRequest_should_success(self):
        """철수의 JWT 로 철수의 작성내역 상세조회 요청을 하면, 성공해야 합니다."""
        # 철수가 작성한 작성내역 리소스(철수가 아이스크림을 사먹음) 를 나타내는 URL 정의
        self.url = reverse(
            "AccountBookHistory-detail", kwargs={"pk": 1, "history_pk": "1"}
        )
        access_token = str(RefreshToken.for_user(self.chulsu).access_token)
        response = self.client.get(
            f"{self.url}",
            HTTP_AUTHORIZATION="Bearer {}".format(access_token),
            content_type="application/json",
        )
        # 철수의 인증 정보와 URL 로 수행되어진 요청은 성공해야 합니다.
        self.assertEqual(response.status_code, 200)

    def test_geumsuJWTDetailRequest_should_fail(self):
        """금수의 JWT 로 철수의 작성내역 상세조회 요청을 하면, 실패해야 합니다."""
        # 철수가 작성한 작성내역 리소스(철수가 아이스크림을 사먹음) 를 나타내는 URL 정의
        self.url = reverse(
            "AccountBookHistory-detail", kwargs={"pk": 1, "history_pk": "1"}
        )
        access_token = str(RefreshToken.for_user(self.geumsu).access_token)
        response = self.client.get(
            f"{self.url}",
            HTTP_AUTHORIZATION="Bearer {}".format(access_token),
            content_type="application/json",
        )
        # 금수의 인증 정보와 URL 로 수행되어진 요청은 실패해야 합니다.
        self.assertEqual(response.status_code, 403)

    def test_chulsuJWTDetailUpdateRequest_should_success(self):
        """철수의 JWT 로 철수의 작성내역 수정 요청을 하면, 성공해야 합니다."""
        # 철수가 작성한 작성내역 리소스(철수가 아이스크림을 사먹음) 를 나타내는 URL 정의
        self.url = reverse(
            "AccountBookHistory-detail", kwargs={"pk": 1, "history_pk": "1"}
        )
        update_data = {
            "memo": "철수가 아이스크림이 아니라 피자를 사먹음",
            "amount": -19000,
            "accountbook": self.chulsu_accountbook_1.id,
        }
        access_token = str(RefreshToken.for_user(self.chulsu).access_token)
        response = self.client.put(
            f"{self.url}",
            update_data,
            HTTP_AUTHORIZATION="Bearer {}".format(access_token),
            content_type="application/json",
        )
        # 철수의 인증 정보와 URL 로 수행되어진 요청은 성공해야 합니다.
        self.assertEqual(response.status_code, 200)

    def test_geumsuJWTDetailUpdateRequest_should_fail(self):
        """금수의 JWT 로 철수의 작성내역 수정 요청을 하면, 실패해야 합니다."""
        # 철수가 작성한 작성내역 리소스(철수가 아이스크림을 사먹음) 를 나타내는 URL 정의
        self.url = reverse(
            "AccountBookHistory-detail", kwargs={"pk": 1, "history_pk": "1"}
        )
        update_data = {
            "memo": "철수가 아이스크림이 아니라 피자를 사먹음",
            "amount": -19000,
            "accountbook": self.chulsu_accountbook_1.id,
        }
        # 철수가 아닌 금수의 JWT
        access_token = str(RefreshToken.for_user(self.geumsu).access_token)
        response = self.client.put(
            f"{self.url}",
            update_data,
            HTTP_AUTHORIZATION="Bearer {}".format(access_token),
            content_type="application/json",
        )
        # 금수의 인증 정보와 URL 로 수행되어진 요청은 실패해야 합니다.
        self.assertEqual(response.status_code, 403)

    def test_chulsuJWTDetailDeleteRequest_should_success(self):
        """철수의 JWT 로 철수의 작성내역 삭제 요청을 하면, 성공해야 합니다."""
        # 철수가 작성한 작성내역 리소스(철수가 아이스크림을 사먹음) 를 나타내는 URL 정의
        self.url = reverse(
            "AccountBookHistory-detail", kwargs={"pk": 1, "history_pk": "1"}
        )
        access_token = str(RefreshToken.for_user(self.chulsu).access_token)
        response = self.client.delete(
            f"{self.url}",
            HTTP_AUTHORIZATION="Bearer {}".format(access_token),
            content_type="application/json",
        )
        # 철수의 인증 정보와 URL 로 수행되어진 요청은 성공해야 합니다.
        self.assertEqual(response.status_code, 204)
        # 삭제가 이루어진 후 데이터베이스에 남아 있는 작성내역의 갯수는 1개여야 합니다.
        self.assertEqual(1, AccountBookHistory.objects.count())

    def test_geumsuJWTDetailDeleteRequest_should_fail(self):
        """금수의 JWT 로 철수의 작성내역 삭제 요청을 하면, 실패해야 합니다."""
        # 철수가 작성한 작성내역 리소스(철수가 아이스크림을 사먹음) 를 나타내는 URL 정의
        self.url = reverse(
            "AccountBookHistory-detail", kwargs={"pk": 1, "history_pk": "1"}
        )
        access_token = str(RefreshToken.for_user(self.geumsu).access_token)
        response = self.client.delete(
            f"{self.url}",
            HTTP_AUTHORIZATION="Bearer {}".format(access_token),
            content_type="application/json",
        )
        # 철수의 인증 정보와 URL 로 수행되어진 요청은 실패해야 합니다.
        self.assertEqual(response.status_code, 403)

```

### accounts 앱의 테스트 케이스

```python
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
```

### 
</details>

### ERD

프로젝트에 사용된 데이터베이스의 구조는 아래와 같습니다.  
![erd](https://user-images.githubusercontent.com/88619089/217833917-6ad1e3e8-8703-4f3a-bf08-247a4b16c7b3.png)



## Getting Started

### Prerequisites

* Python3.8 혹은 이후의 버전이 필요합니다.
  ```sh
  python3 --version
  ```
  Python 버전이 3.8 이상임을 꼭 확인해 주세요.
* mysql 서버가 열려 있어야 하고, config/development.py 에 정의된 설정으로 구성되어 있어야 합니다.
* redis 서버가 열려 있어야 합니다.

### Installation

1. 저장소를 클론합니다.
   ```sh
   git clone https://github.com/github_username/repo_name.git
   ```
2. 가상환경을 생성합니다..
   ```sh
   python3 -m venv venv
   ```
3. pip 업데이트를 진행합니다.
   ```sh
   pip install --upgrade pip
   ```
4. 필요한 Python 패키지들을 설치합니다.
   ```sh
   pip install -r requirements.txt
   ```
5. 로컬 Django 서버를 구동합니다.
   ```sh
   python3 manage.py runserver
   ```
6. 작성한 테스트 케이스에 대해서는 아래의 명령어를 입력하여 테스트를 진행할 수 있습니다.
   ```sh
   python3 manage.py test --settings config.settings.testing
   ```



## REST API Specification
작성한 API 의 스펙을 소개합니다.
https://documenter.getpostman.com/view/21924519/2s935smgb8  
에서 전체 문서를 확인할 수 있습니다.


## Features

- [X] 이메일, 비밀번호를 통한 회원가입 구현
    - [X] Django 기본 사용자 모델이 아닌 커스텀 유저 모델 생성하기
    - [X] `POST /api/v1/accounts/register/` 로 회원가입 API 구현하기
- [X] JWT 인증을 통한 로그인 & 로그아웃 구현
    - [X] `POST /api/v1/jwtauth/login/` 로 로그인 API 구현하기 (`access token` 발급)
    - [X] `POST /api/v1/jwtauth/refresh/` 로 로그인 API 구현하기 (`access token` 재발급)
    - [X] `POST /api/v1/jwtauth/logout/` 로 로그아웃 API 구현하기 (블랙리스트)
- [X] 가계부 서비스 구현
    - [X] 가계부들에 대한 리소스: `/api/v1/accountbooks/`
      - [X] `GET` => 사용자의 모든 가계부 목록 조회 API 구현하기 (본인의 가계부 목록만 확인할 수 있음)
      - [X] `POST` => 가계부 생성 API 구현하기 (로그인 한 상태에서만 생성할 수 있음)
    - [X] 특정 가계부에 대한 리소스: `/api/v1/accountbooks/{int:id}/`
      - [X] `GET` => 특정 가계부 상세조회 API 구현하기 (로그인한 상태에서만 조회할 수 있음)
      - [X] `PUT` => 특정 가계부에 수정 API 구현하기 (제목만 수정할 수 있음)
      - [X] `DELETE` => 특정 가계부 삭제 API 구현하기 (본인의 가계부만 삭제할 수 있음)
    - [X] 작성내역들에 대한 리소스: `/api/v1/accountbooks/{int:id}/histories/`
      - [X] `GET` => 작성내역 조회 API 구현하기 (본인의 가계부 목록만 확인할 수 있음)
      - [X] `POST` => 작성내역 생성 API 구현하기 (로그인 한 상태에서만 생성할 수 있음)
    - [X] 특정 작성내역에 대한 리소스: `/api/v1/accountbooks/{int:id}/histories/{int:id}/`
      - [X] `GET` => 특정 작성내역 상세조회 API 구현하기 (로그인한 상태에서, 본인만 조회할 수 있음)
      - [X] `PUT` => 특정 작성내역 수정 API 구현하기 (제목만 수정할 수 있음)
      - [X] `DELETE` => 특정 작성내역 삭제 API 구현하기 (본인의 가계부만 삭제할 수 있음)
  - [X] 가계부의 특정 세부 내역을 공유할 수 있게 단축 URL을 만들 수 있습니다.
  - [ ] 가계부의 세부 내역을 복제할 수 있습니다.


## Things I have considered
구현을 진행하며 고민되었던 점들을 소개합니다.

#### 프로젝트 레이아웃을 어떻게 구성할 것인가?
- 제가 구성한 프로젝트 구조는 아래와 같습니다.
```
pay_right_here
├── __init__.py
├── accountbook
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── migrations
│   │   ├── 0001_initial.py
│   │   ├── 0002_remove_accountbook_uuid.py
│   │   └── __init__.py
│   ├── models.py
│   ├── permissions.py
│   ├── serializers.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── accounts
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── migrations
│   │   ├── 0001_initial.py
│   │   └── __init__.py
│   ├── models.py
│   ├── serializers.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
└── jwtauth
    ├── __init__.py
    ├── admin.py
    ├── apps.py
    ├── jwt.py
    ├── migrations
    │   └── __init__.py
    ├── models.py
    ├── tests.py
    ├── urls.py
    └── views.py
```

- Config 라는 프로젝트 폴더를 구성하고, pay_right_here 이라는 패키지 안에 세 개의 앱을 위치하였습니다. 각각의 앱은 다음의 역할을 가집니다.
  - accounts : 회원가입을 수행합니다.
  - jwtauth : 액세스 토큰 발급, 리프레시 토큰 발급, 리프레시 토큰 로테이션을 수행합니다.
  - accountbook : 가계부 서비스를 수행합니다.
- 이렇게 처음 구성해보았지만 좋았던 점은 `apps` 와 같은 추상적인 폴더명 대신 `pay_right_here` 와 같이 명확한 폴더명을 사용하였기에 구현 시, 그리고 작업 시 조금 더 명확한 분리가 가능했다는 점이었습니다.

#### 비즈니스 로직은 어디에 위치해야 하는가?
- Django 에서의 비즈니스 로직 분리는 정말 고민되었던 것 같습니다.
- 왜냐하면, 제 생각에는 Serializer 와 Model 에서 비즈니스 로직을 일부 처리하고 있다고 생각했기 때문입니다.
- 최대한, Django REST Framework 의 Serializer 를 활용하고, Fat Model 개념을 준수하자고 생각하며 코드를 작성했습니다.
- 그러므로 현재는 별도로 구성된 Service Layer 는 존재하지 않습니다.

#### 사용자는 몇 개의 가계부를 가질 수 있는가?
- 사용자는 여러 개의 가계부를 작성할 수 있다고 가정하였습니다.
- 그렇기 때문에, 가계부 자체에 대한 CRUD API 의 구현이 선행되어야 했습니다.
- 그 이후, 가계부에 작성하는 작성내역 API 를 구현하였습니다.

#### 로그아웃은 어떻게 구현되어야 하는가?
- 맨 처음에는 요구사항을 확인했을 때 당황했습니다. 왜냐하면 로그아웃은 프론트엔드 단에서 처리하는 것으로 알고 있었기 때문입니다.
- 예를 들어서, 백엔드 서버가 토큰을 발급해 준다면 토큰은 만료되기 전까지 유효하기 때문에, 만약 프론트엔드 단에서 토큰을 로컬스토리지에 저장했다면 그것을 브라우저에서 지움으로서 로그아웃이 이루어진다고 생각했습니다.
- 하지만, 특정 토큰의 정보를 블랙리스트로 관리할 수 있다는 것을 알게 되었고, 관련 라이브러리를 사용하여 구현을 진행했습니다.
- 저의 구현에서는, `/logout/` 과 같은 엔드포인트에 사용자가 `refresh token` 을 담아 요청을 보낸다면, 해당 토큰을 블랙리스트에 올리는 방식으로 구현했습니다. 결과적으로, 사용자의 로그아웃은 아래와 같은 순서로 이루어집니다.
  1. 사용자(클라이언트) 는 로그아웃 엔드포인트에 `refresh token` 을 담아 요청을 보내고, 브라우저의 로컬스토리지 등에서 토큰을 삭제합니다.
  2. 서버는 전송된 리프레시 토큰을 블랙리스트에 올리고, 나중에 해당 리프레시 토큰을 다시 사용할 수 없도록 합니다.
  3. 결과적으로, 사용자는 나중에 다시 로그인을 해야 합니다. 액세스 토큰이 브라우저에서 삭제되지 않았더라도, 액세스 토큰의 만료기간이 지나면 리프레시 토큰을 다시 사용할 수 없으므로 재로그인을 해야만 서비스 이용이 가능합니다.

#### 추후의 확장을 위해서, 가계부 리소스에 대한 모든 엔드포인트를 구현했습니다.
- 예를 들면, 만약 "가계부 상세조회" 서비스에서 "이 가계부에 작성된 작성내역은 총 몇 개입니다." 라는 추가적인 정보가 필요하다면, 언제든지 추가할 수 있습니다.

#### 코드가 명백하게 동작하는 것을 보장해주는 테스트 코드의 케이스를 자세하게 작성했습니다.
- 각각의 어플리케이션의 `tests.py` 파일을 확인하시면 어떻게 테스트 코드를 구성했는지 확인하실 수 있습니다.

#### 가계부 복제란 무엇인가?
- 이것 또한 당황한 포인트 중 하나였습니다. 복제라는 것은 어떤 것을 말하는 것인지 쉬이 떠올리기 어려웠기 때문입니다.
- 제가 해석한 복제는, "내가 작성한 작성내역 1의 내용을 복제하여 어딘가에 따로 저장해두는 것" 이었습니다.
- 다만, 같은 데이터베이스를 생성할 필요는 없다고 생각하였고 상세내용을 JSON 그대로 어딘가에 저장해두는 것을 선택하였습니다.
- 결과적으로, 사용자는 복제하고자 하는 상세내용을 body 에 담아 `POST /accountbook/copies/` 요청을 보내면 해당 내용을 복제할 수 있도록 구현하고 싶었습니다.
- 현재는 데이터베이스만 적용된 상태입니다.



[Python3]: https://img.shields.io/badge/python3-3776AB?style=for-the-badge&logo=python&logoColor=white
[Python3-url]: https://www.python.org/
[Django]: https://img.shields.io/badge/django-092E20?style=for-the-badge&logo=django&logoColor=white
[Django-url]: https://www.djangoproject.com/
[MySQL]: https://img.shields.io/badge/mysql-4479A1?style=for-the-badge&logo=mysql&logoColor=white
[MySQL-url]: https://www.mysql.com/

