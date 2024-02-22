from django.contrib import admin
from django.urls import path,include
from cafe.views import home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('api/cafe/v1/', include('cafe.urls')),
]
# http://127.0.0.1:8000/api/cafe/v1/chatgpt/