from django.urls import path, include
from .views import CafeOwnerRegisterView,CustomLoginView

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('register/', CafeOwnerRegisterView.as_view(), name='register'),
]