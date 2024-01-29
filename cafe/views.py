from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import ValidationError
from google.cloud import texttospeech
from django.http import JsonResponse
from django.contrib.auth import login as django_login, authenticate
from django.shortcuts import render,redirect
import openai
from django.conf import settings
import os
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

def get_completion2(request, user_input): 
    # 대화 이력 확인 및 업데이트
    if 'history' not in request.session:
        request.session['history'] = []

    # 이전 대화 내역을 포함시킴
    previous_conversation = "\n".join([f"{exchange['user']}\\n{exchange['bot']}" for exchange in request.session['history']])
    full_prompt = previous_conversation + "\n\n" + user_input

    # OpenAI GPT 모델을 사용하여 대답 생성
    query = openai.ChatCompletion.create( 
        model="gpt-3.5-turbo",
        messages=[
            {'role':'user','content': full_prompt}
        ], 
        max_tokens=1024, 
        n=1, 
        stop=None, 
        temperature=0.5, 
    ) 
    response = query.choices[0].message["content"]

    # 새 대화 내역 추가
    request.session['history'].append({'user': user_input, 'bot': response})
    
    return response

def run_text_to_speech(text, post_count):
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="/Users/jeonjisu/Desktop/university/project/BongABang-FishBread-server/codebook/bong-a-bang-412508-9e4d0ff505ce.json"
    client = texttospeech.TextToSpeechClient()
    synthesis_input = texttospeech.SynthesisInput(text=text)
    voice = texttospeech.VoiceSelectionParams(
        language_code="ko-KR", ssml_gender=texttospeech.SsmlVoiceGender.FEMALE
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )
    
    # 새로운 파일 이름 생성
    output_file_name = f"newoutput_v{post_count}.mp3"
    output_file_path = os.path.join(settings.MEDIA_ROOT, output_file_name)
    print("output_file_path",output_file_path)
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    # 새로운 파일로 오디오 저장
    with open(output_file_path, "wb") as out:
        out.write(response.audio_content)
        print(f'Audio file Created !  "{output_file_path}"')

    # 새로운 파일 이름과 경로를 반환
    return output_file_name, output_file_path
def query_view2(request): 
    if request.method == 'POST': 
        user_input = request.POST.get('prompt') 
        user_input = str(user_input)
        response = get_completion2(request, user_input)
        
        # 새로운 파일 이름을 얻어옴
        post_count = request.session.get('post_count', 0)
        post_count += 1
        request.session['post_count'] = post_count
        new_audio_file_name, new_audio_file_path = run_text_to_speech(response, post_count)
        print("settings.MEDIA_URL",settings.MEDIA_URL)
        audio_url = request.build_absolute_uri(settings.MEDIA_URL + new_audio_file_name)

        return JsonResponse({'response': response, 'audio_url': audio_url, 'history': request.session['history']})
    elif request.method == 'GET':
        # GET 요청 시 대화 세션 초기화
        request.session['started'] = False
        request.session['history'] = []
        request.session['post_count'] = 0
    return render(request, 'query.html', {'history': request.session.get('history', [])})
