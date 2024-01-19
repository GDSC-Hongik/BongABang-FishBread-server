from django.contrib.auth.models import AbstractUser
from django.db import models

class CafeOwner(AbstractUser):
    phone_number = models.CharField(max_length=15, blank=True)  # 유저 전화번호 필드 추가
    email = models.EmailField(unique=True)  # 중복된 이메일 주소 허용 x
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone_number'] # 회원가입시 적어야 하는 필드. username_field는 적지 않아야함.
    def __str__(self):
        return self.username

class Cafe(models.Model):
    owner = models.ForeignKey(CafeOwner, on_delete=models.CASCADE)
    cafe_name = models.CharField(max_length=100)
    cafe_address = models.CharField(max_length=255)
    cafe_phone_number = models.CharField(max_length=15)

    def __str__(self):
        return self.cafe_name
    
class Menu(models.Model):
    cafe = models.ForeignKey(Cafe, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    price_ice = models.IntegerField()
    price_hot = models.IntegerField()
    price_constant = models.IntegerField()
    menu_type = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='menu_images/')

    def __str__(self):
        return self.name