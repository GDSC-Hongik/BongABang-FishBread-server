from django.urls import path, include
from .views import CafeOwnerRegisterView,CustomLoginView,register,login,\
    home,cafe_menu,some_menu,query_view, RealTimeSTT, transcribe_audio

urlpatterns = [
    # path('login/', CustomLoginView.as_view(), name='register'),
    # path('register/', CafeOwnerRegisterView.as_view(), name='register'),
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('cafe_menu/', cafe_menu, name='cafe_menu'),
    path('some_menu/', some_menu, name='some_menu'),
    path('chatgpt/',query_view, name='query_view'),
    path('stt/',RealTimeSTT,name='stt'),
    path('transcribe_audio',transcribe_audio,name='transcribe_audio'),
    path('', home, name='home'),
]
