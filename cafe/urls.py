from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import TranscribeAudioView,SpeechToTextView,MenuListView, QueryView,CafeOwnerRegisterView,CustomLoginView,register,login,cafe_menu,some_menu,cafe_menu,some_menu, transcribe_audio
urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('cafe_menu/', cafe_menu, name='cafe_menu'),
    path('some_menu/', some_menu, name='some_menu'),
    path('chatgpt/',QueryView.as_view(), name='query_view'),
    path('stt/',TranscribeAudioView.as_view(),name='stt'),
    path('tts/',SpeechToTextView.as_view(),name='stt'),
    path('transcribe_audio',transcribe_audio,name='transcribe_audio'),
    path('menus/', MenuListView.as_view(), name='menu-list'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
