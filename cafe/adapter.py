from allauth.account.adapter import DefaultAccountAdapter
from allauth.account.utils import user_field

class CustomUserAccountAdapter(DefaultAccountAdapter):
    def save_user(self, request, user, form, commit=False):
        user = super().save_user(request, user, form, commit)
        
        # 사용자의 이름과 휴대폰 번호 저장
        user_field(user, 'owner_phone_number', request.data.get('owner_phone_number'))
        user_field(user, 'owner_name', request.data.get('owner_name'))
        user_field(user, 'cafe_name', request.data.get('cafe_name'))
        user_field(user, 'cafe_address', request.data.get('cafe_address'))
        user_field(user, 'cafe_phone_number', request.data.get('cafe_phone_number'))
        
        user.save()
        return user