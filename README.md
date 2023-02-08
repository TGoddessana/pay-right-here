<div align="center">

<h1 align="center">Pay Right Here! - Backend</h1>
  <p align="center">
    소비하고, 기록하고, 찾아보세요. 바로 여기서!
    <br />
    가계부 서비스를 위한 REST API 입니다.
    <br />
    <a href=""><strong>REST API 명세서 »</strong></a>
    <br />
    <br />
  </p>
</div>



<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#rest-api-specification">REST API Specification</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
  </ol>
</details>



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

### ERD

프로젝트에 사용된 데이터베이스의 구조는 아래와 같습니다.



## Getting Started

### Prerequisites

* Python3.8 혹은 이후의 버전이 필요합니다.
  ```sh
  python --version
  ```
  Python 버전이 3.8 이상임을 꼭 확인해 주세요.

### Installation

1. 저장소를 클론합니다.
   ```sh
   git clone https://github.com/github_username/repo_name.git
   ```
2. pip 업데이트를 진행합니다.
   ```sh
   pip install --upgrade pip
   ```
3. 필요한 Python 패키지들을 설치합니다.
   ```sh
   pip install -r requirements.txt
   ```



## REST API Specification
작성한 API 의 스펙을 소개합니다.



## Roadmap

- [X] 이메일, 비밀번호를 통한 회원가입 구현
    - [X] Django 기본 사용자 모델이 아닌 커스텀 유저 모델 생성하기
    - [X] `POST /api/v1/accounts/register/` 로 회원가입 API 구현하기
- [ ] 회원탈퇴 구현
    - [ ] JWT 와 함께 request 를 받았을 때에만, 본인만 회원탈퇴가 가능하도록 구현하기    
- [ ] JWT 인증을 통한 로그인 & 로그아웃 구현
    - [ ] `POST /api/v1/jwtauth/login/` 로 로그인 API 구현하기 (`access token` 발급)
    - [ ] `POST /api/v1/jwtauth/refresh/` 로 로그인 API 구현하기 (`access token` 재발급)
    - [ ] `POST /api/v1/jwtauth/logout/` 로 로그아웃 API 구현하기 (블랙리스트)
- [ ] 가계부 서비스 구현
    - [ ] 가계부에 오늘 사용한 돈의 금액과 관련된 메모를 남길 수 있습니다. 
    - [ ] 가계부에서 수정을 원하는 내역은 금액과 메모를 수정 할 수 있습니다.
    - [ ] 가계부에서 삭제를 원하는 내역은 삭제 할 수 있습니다.
    - [ ] 가계부에서 이제까지 기록한 가계부 리스트를 볼 수 있습니다. 
    - [ ] 가계부에서 상세한 세부 내역을 볼 수 있습니다. 
    - [ ] 가계부의 세부 내역을 복제할 수 있습니다.
    - [ ] 가계부의 특정 세부 내역을 공유할 수 있게 단축 URL을 만들 수 있습니다.
 


## Things I have considered
구현을 진행하며 고민되었던 점들을 소개합니다.



[Python3]: https://img.shields.io/badge/python3-3776AB?style=for-the-badge&logo=python&logoColor=white
[Python3-url]: https://www.python.org/
[Django]: https://img.shields.io/badge/django-092E20?style=for-the-badge&logo=django&logoColor=white
[Django-url]: https://www.djangoproject.com/
[MySQL]: https://img.shields.io/badge/mysql-4479A1?style=for-the-badge&logo=mysql&logoColor=white
[MySQL-url]: https://www.mysql.com/

