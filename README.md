## 개발 환경

---

주요 환경 목록

- python (3.9.11)
- Django (4.0)
- python-dotenv(1.0.1)
- openai(0.28.1)
- google-cloud-speech==2.23.0

기타 환경 설정 설치

```python
pip install -r requirements.txt
```

## 실행 방법

---

- Git에서 해당 레포지토리의 최신 코드를 clone 한다.

```python
https://github.com/GDSC-Hongik/BongABang-FishBread-server.git
```

- db에 접속하기 위해 .env 파일을 작성해야 한다. 파일에 들어갈 내용은 다음과 같다. 해당 내용들을 빠짐없이 작성해야 한다. (.env 파일의 위치는 [manage.py](http://manage.py) 위치와 동일해야 한다.)
    - api-key
    - DB_ENGINE
    - DB_NAME
    - DB_USER
    - DB_PASSWORD
    - DB_HOST
    - DB_PORT
    - GOOGLE_APPLICATION_CREDENTIALS
- `python [manage.py](http://manage.py) runserver` 을 실행한다.
- https://127.0.0.1:8000/ 화면이 오류없이 출력되는지 확인한다.