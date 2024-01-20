from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.db import models
from .managers import CafeOwnerManager

class CafeOwner(AbstractUser, PermissionsMixin):
    username = None
    first_name = None
    last_name = None
    # 유저 정보
    email = models.EmailField(unique=True)
    owner_phone_number = models.CharField(max_length=15, blank=True, null=True)
    owner_name = models.CharField(max_length=30, blank=True)
    
    # 카페 정보
    cafe_name = models.CharField(max_length=100)
    cafe_address = models.CharField(max_length=255)
    cafe_phone_number = models.CharField(max_length=15)
    cafe_image = models.ImageField(upload_to='menu_images', default='default_image.jpg')
    
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['owner_phone_number','owner_name','cafe_name','cafe_address','cafe_phone_number']

    objects = CafeOwnerManager()

    def __str__(self):
        return self.email
    
