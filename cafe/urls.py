from django.urls import path, include
from .views import CafeOwnerRegisterView,CustomLoginView,register,login,home

urlpatterns = [
    # path('login/', CustomLoginView.as_view(), name='register'),
    # path('register/', CafeOwnerRegisterView.as_view(), name='register'),
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('', home, name='home'),
    
]