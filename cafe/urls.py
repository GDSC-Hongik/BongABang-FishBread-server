from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import CafeOwnerRegisterView,CustomLoginView,register,login,home,query_view,cafe_menu,some_menu,get_audio_file,get_latest_audio
urlpatterns = [
    # path('login/', CustomLoginView.as_view(), name='register'),
    # path('register/', CafeOwnerRegisterView.as_view(), name='register'),
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('cafe_menu/', cafe_menu, name='cafe_menu'),
    path('some_menu/', some_menu, name='some_menu'),
    path('chatgpt/',query_view, name='query_view'),
    path('', home, name='home'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)