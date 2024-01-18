from django.urls import path, include
from .views import CustomLoginView

urlpatterns = [
    path('', include('dj_rest_auth.urls')),
    path('registration/', include('dj_rest_auth.registration.urls')),
    path('login/', CustomLoginView.as_view(), name='custom_login'),
]