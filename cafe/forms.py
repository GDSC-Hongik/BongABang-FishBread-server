from allauth.account.forms import SignupForm
from django import forms
from .models import CafeOwner
class CustomSignupForm(SignupForm):
    # 기본 User 모델 필드
    email = forms.EmailField(label='Email', required=True)
    password = forms.CharField(widget=forms.PasswordInput, label='Password', required=True)
    username = forms.CharField(max_length=150, label='Username', required=True)
    first_name = forms.CharField(max_length=30, label='First Name', required=True)
    last_name = forms.CharField(max_length=30, label='Last Name', required=True)

    phone_number = forms.CharField(max_length=15, label='Phone Number', required=True)

    class Meta:
        model = CafeOwner
        fields = ('username', 'email', 'password1', 'password2', 'first_name', 'last_name', 'phone_number')