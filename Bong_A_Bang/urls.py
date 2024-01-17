from django.contrib import admin
from django.urls import path,include,re_path
from rest_auth import rest_auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^rest-auth/', include('rest_auth.urls')),
    path('', include('cafe.urls')),
]
