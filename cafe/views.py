import openai
import os
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import ValidationError
from django.http import JsonResponse
from django.contrib.auth import login as django_login, authenticate
from django.shortcuts import render,redirect
from django.views import View
from django.conf import settings
from .models import Menu
from .serializers import CafeOwnerRegisterSerializer,CustomLoginSerializer

class CafeOwnerRegisterView(APIView):
    permission_classes = [AllowAny]
    def post(self, request, *args, **kwargs):
        serializer = CafeOwnerRegisterSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            return Response({"message": "사용자가 성공적으로 생성되었습니다."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class CustomLoginView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = CustomLoginSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            user = serializer.validated_data
            refresh = RefreshToken.for_user(user)

            return Response({
                'access_token': str(refresh.access_token),
                'refresh_token': str(refresh),
            }, status=status.HTTP_200_OK)
            
def register(request):
    if request.method == 'POST':
        print("post")
        serializer = CafeOwnerRegisterSerializer(data=request.POST)
        if serializer.is_valid():
            serializer.save()
            return render(request, 'login.html')
        return redirect('/api/cafe/v1/register/')
    else:
        print(request.method)
        print("예외")
        return render(request, 'register.html')
def login(request):
    if request.method == 'POST':
        print("또 post")
        serializer = CustomLoginSerializer(data=request.POST)
        if serializer.is_valid():
            user = serializer.validated_data
            django_login(request, user)
            print("로그인성공")
            return redirect('api/cafe/v1/') 
        else:
            print("로그인실패")
            return render(request, 'login.html', {'error_message': '유효하지 않은 로그인 정보입니다.'})
    else:
        # GET 요청인 경우, 로그인 폼을 보여줌
        print("또 get")
        return render(request, 'login.html')

def home(request):
    return render(request, 'index.html')

def cafe_menu(request):
    cafe_menu_items = Menu.objects.all()
    return render(request, 'cafe_menu.html', {'cafe_menu': cafe_menu_items})

def some_menu(request):
    menus = Menu.objects.filter(price_ice__gte=3000)
    return render(request, 'cafe_menu.html', {'cafe_menu': menus})

# chatgpt 연동
def get_completion(prompt): 
	print(prompt) 
	query = openai.ChatCompletion.create( 
		model="gpt-3.5-turbo",
		messages=[
        	{'role':'user','content': prompt}
    	], 
		max_tokens=1024, 
		n=1, 
		stop=None, 
		temperature=0.5, 
	) 
	response = query.choices[0].message["content"]
	print(response) 
	return response 


def query_view(request): 
	if request.method == 'POST': 
		prompt = request.POST.get('prompt') 
		prompt=str(prompt)
		response = get_completion(prompt)
		return JsonResponse({'response': response}) 
	return render(request, 'query.html') 

def RealTimeSTT(request):
    return render(request,'stt.html')

from google.protobuf.json_format import MessageToDict
from google.cloud import speech
from datetime import datetime

def transcribe_audio(request):
    if request.method == 'POST':
        # Audio recording parameters
        RATE = 16000
        CHUNK = int(RATE / 10)  # 100ms

        if 'audio' in request.FILES:
            audio_file = request.FILES['audio']

            # 로컬 디렉터리에 저장 (media/audio/ 하위에 저장됨)
            # 현재 시간을 기반으로 파일 이름 생성
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            file_name = f"audio_{timestamp}.wav"
            file_path = os.path.join(settings.MEDIA_ROOT, 'audio', file_name)
            with open(file_path, 'wb') as destination:
                for chunk in audio_file.chunks():
                    destination.write(chunk)

            client = speech.SpeechClient()

            with open(file_path, "rb") as audio_file_2:
                content = audio_file_2.read()

            audio = speech.RecognitionAudio(content=content)
            config = speech.RecognitionConfig(
                encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
                sample_rate_hertz=48000,
                language_code="ko-KR",
            )

            response = client.recognize(config=config, audio=audio)
            print(response)
            # Each result is for a consecutive portion of the audio. Iterate through
            # them to get the transcripts for the entire audio file.
            transcripts = [result.alternatives[0].transcript for result in response.results]

            return JsonResponse({'status': 'success', 'transcripts': transcripts})
        else:
            return JsonResponse({'status': 'error', 'message': 'No audio file provided'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})
#             # Set the language code accordingly
#             language_code = "ko-KR"  # a BCP-47 language tag

#             config = speech.RecognitionConfig(
#                 encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16, 
#                 sample_rate_hertz=RATE,
#                 language_code=language_code,
#                 enable_automatic_punctuation=True,
#             )

#             audio_content = buff.getvalue()

#             # Use the Google Cloud Speech-to-Text API
#             audio = speech.RecognitionAudio(content=audio_content)
#             streaming_config = speech.StreamingRecognitionConfig(
#                 config=config, interim_results=True
#             )

#             requests = [speech.StreamingRecognizeRequest(audio_content=audio_content)]

#             responses = client.streaming_recognize(streaming_config, requests)

#             # Process the transcription responses
#             transcript = listen_print_loop(responses)

#             # Return the transcript as JSON
#             return JsonResponse({'transcript': transcript})

#     return JsonResponse({'error': 'Invalid request method'})

# def listen_print_loop(responses):
#     """Iterates through server responses and returns the transcript."""
#     transcript = ""

#     for response in responses:
#         if not response.results:
#             continue

#         result = response.results[0]
#         if not result.alternatives:
#             continue

#         # Display the transcription of the top alternative.
#         transcript += result.alternatives[0].transcript + " "
    
#     return transcript.strip()

# from django.views.decorators.http import require_POST
# from django.conf import settings

# @require_POST
# def upload_audio(request):
#     if 'audio' in request.FILES:
#         audio_file = request.FILES['audio']

#         # 로컬 디렉터리에 저장 (media/audio/ 하위에 저장됨)
#         with open(os.path.join(settings.MEDIA_ROOT, 'audio', 'audio.wav'), 'wb') as destination:
#             for chunk in audio_file.chunks():
#                 destination.write(chunk)

#         return JsonResponse({'status': 'success'})
#     else:
#         return JsonResponse({'status': 'error', 'message': 'No audio file provided'})
