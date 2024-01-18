from dj_rest_auth.serializers import LoginSerializer
from rest_framework import serializers


class CustomLoginSerializer(LoginSerializer):
    email = serializers.CharField(required=True, allow_blank=False)
    password = serializers.CharField(style={'input_type': 'password'})