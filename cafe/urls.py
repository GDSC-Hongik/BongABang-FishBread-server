from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import TranscribeAudioView,SpeechToTextView,MenuListView,RegisterView, QueryView,CafeOwnerRegisterView,LoginAPIView,CustomLoginView,transcribe_audio
urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('chatgpt/',QueryView.as_view(), name='query_view'),
    path('stt/',TranscribeAudioView.as_view(),name='stt'),
    path('tts/',SpeechToTextView.as_view(),name='stt'),
    path('transcribe_audio/',transcribe_audio,name='transcribe_audio'),
    path('menus/', MenuListView.as_view(), name='menu-list'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
