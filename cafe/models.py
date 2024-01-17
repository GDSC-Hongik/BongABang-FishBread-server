from django.contrib.auth.models import User
from django.db import models

class CafeOwner(User):
    email = models.EmailField(unique=True)
    user_name = models.CharField(max_length=30, unique=True)  # 유저 이름 필드 추가
    phone_number = models.CharField(max_length=15, blank=True)  # 유저 전화번호 필드 추가

    def __str__(self):
        return self.username

class Cafe(models.Model):
    owner = models.ForeignKey(CafeOwner, on_delete=models.CASCADE)
    cafe_name = models.CharField(max_length=100)
    cafe_address = models.CharField(max_length=255)
    cafe_phone_number = models.CharField(max_length=15)

    def __str__(self):
        return self.cafe_name