from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from .models import Menu

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
                print("사용자는 있음")
                if not user.is_active:
                    print("사용자는 비활성화상태")
                    raise serializers.ValidationError("이 사용자 계정은 비활성화 상태입니다.")
                return user
            else:
                print("이메일과 비밀번호가 일치하지 않습니다")
                raise serializers.ValidationError("이메일과 비밀번호가 일치하지 않습니다.")
        else:
            raise serializers.ValidationError("이메일과 비밀번호를 모두 입력해야 합니다.")

        return data
    
class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = '__all__'