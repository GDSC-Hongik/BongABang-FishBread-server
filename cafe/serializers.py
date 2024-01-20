# from dj_rest_auth.serializers import LoginSerializer
# from rest_framework import serializers
# from dj_rest_auth.registration.serializers import RegisterSerializer
# from django.core.validators import RegexValidator

# 로그인
# class CustomLoginSerializer(LoginSerializer):
#     email = serializers.CharField(required=True, allow_blank=False)
#     password = serializers.CharField(style={'input_type': 'password'})

# # 회원가입
# class CustomRegisterSerializer(RegisterSerializer):
#     owner_name = serializers.CharField(max_length=30, write_only=True, required=True, help_text="이름")
#     cafe_name = serializers.CharField(max_length=100, write_only=True, required=True, help_text="카페 이름")
#     cafe_address = serializers.CharField(max_length=255, write_only=True, required=True, help_text="카페 주소")
#     cafe_phone_number = serializers.CharField(max_length=15, write_only=True, required=True, help_text="카페 전화번호")
#     phoneNumberRegex = RegexValidator(regex=r'^01([0|1|6|7|8|9]?)-?([0-9]{3,4})-?([0-9]{4})$')
#     owner_phone_number = serializers.CharField(validators=[phoneNumberRegex],help_text="휴대폰 번호는 다음과 같은 형식을 따라야 합니다: 010-1234-5678")
    
#     def save(self, request):
#         user = super().save(request)

#         owner_name = self.validated_data.get('owner_name')
#         owner_phone_number = self.validated_data.get('owner_phone_number')
#         cafe_name = self.validated_data.get('cafe_name')
#         cafe_address = self.validated_data.get('cafe_address')
#         cafe_phone_number = self.validated_data.get('cafe_phone_number')

#         user.owner_name = owner_name
#         user.owner_phone_number = owner_phone_number
#         user.cafe_name = cafe_name
#         user.cafe_address = cafe_address
#         user.cafe_phone_number = cafe_phone_number
#         user.save()
#         return user

from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate

class CafeOwnerRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('email', 'owner_phone_number', 'owner_name', 'cafe_name', 'cafe_address', 'cafe_phone_number', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = get_user_model().objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            owner_phone_number=validated_data.get('owner_phone_number'),
            owner_name=validated_data.get('owner_name'),
            cafe_name=validated_data.get('cafe_name'),
            cafe_address=validated_data.get('cafe_address'),
            cafe_phone_number=validated_data.get('cafe_phone_number')
        )
        return user
class CustomLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(style={'input_type': 'password'})

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if email and password:
            user = authenticate(email=email, password=password)
            if user:
                if not user.is_active:
                    raise serializers.ValidationError("이 사용자 계정은 비활성화 상태입니다.")
                return user
            else:
                raise serializers.ValidationError("이메일과 비밀번호가 일치하지 않습니다.")
        else:
            raise serializers.ValidationError("이메일과 비밀번호를 모두 입력해야 합니다.")

        return data