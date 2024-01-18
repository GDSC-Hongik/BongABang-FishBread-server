from django.contrib.auth.models import AbstractUser, BaseUserManager

class CafeOwnerManager(BaseUserManager):
    def create_user(self, email, password=None, owner_phone_number=None, owner_name=None, \
        cafe_name=None, cafe_address=None, cafe_phone_number=None, **extra_fields):
        """
        일반 사용자 생성 메서드
        """
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        
        # CafeOwner 정보 생성
        user = self.model(email=email, owner_phone_number=owner_phone_number,\
            owner_name=owner_name, cafe_name=cafe_name, cafe_address= cafe_address,\
                cafe_phone_number=cafe_phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None,**extra_fields):
        """
        슈퍼유저(관리자) 생성 메서드
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)