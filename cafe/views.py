from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import ValidationError
from google.cloud import texttospeech
from django.http import JsonResponse, FileResponse,HttpResponseNotFound
from django.contrib.auth import login as django_login, authenticate
from django.shortcuts import render,redirect
import openai
from datetime import datetime

from django.conf import settings
import os, re
from .models import Menu
from .serializers import CafeOwnerRegisterSerializer,CustomLoginSerializer

def get_audio_file(request, file_name):
    file_path = os.path.join(settings.MEDIA_ROOT, file_name)

    if os.path.exists(file_path):
        return FileResponse(open(file_path, 'rb'))
    else:
        return HttpResponseNotFound("The requested audio file was not found.")

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

def get_latest_audio(request):
    static_dir = 'static/'  # 정적 파일 폴더 경로
    audio_files = [f for f in os.listdir(static_dir) if f.endswith('.mp3')]

    # 파일명에서 숫자 추출 및 정렬
    audio_files.sort(key=lambda f: int(re.search("v(\d+)", f).group(1)), reverse=True)

    if audio_files:
        latest_file = audio_files[0]  # 가장 큰 숫자를 가진 파일
        print(latest_file)
        return JsonResponse({'latest_audio': latest_file})
    else:
        print("no latest_file")
        return JsonResponse({'error': 'No audio files found'})

def get_completion(request, user_input): 
    # 대화 이력 확인 및 업데이트
    if 'history' not in request.session:
        request.session['history'] = []

    # 이전 대화 내역을 포함시킴
    previous_conversation = "\n".join([f"{exchange['user']}\\n{exchange['bot']}" for exchange in request.session['history']])
    full_prompt = previous_conversation + "\n\n" + user_input
    print("full_prompt:",full_prompt)
    # OpenAI GPT 모델을 사용하여 대답 생성
    query = openai.ChatCompletion.create( 
        model="gpt-3.5-turbo",
        messages=[
            {'role':'user','content': full_prompt}
        ], 
        max_tokens=1024, 
        n=1, 
        stop=None, 
        temperature=0.1, 
    ) 
    response = query.choices[0].message["content"]

    # 새 대화 내역 추가
    request.session['history'].append({'user': user_input, 'bot': response})
    print(response)
    return response

def run_text_to_speech(text, post_count,now):
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
    output_file_name = f"newoutput_v{post_count}{now}.mp3"
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
def query_view(request):
    print(request.method)
    if request.method == 'POST':
        user_input = request.POST.get('prompt')
        user_input = str(user_input)
        print("user_input",user_input)
        # 사용자 입력이 유효한 경우에만 음성 파일 생성 로직 실행
        if user_input:
            response = get_completion(request, user_input)
            now = str(datetime.now())

            # 새로운 파일 이름을 얻어옴
            post_count = request.session.get('post_count', 0)
            post_count += 1
            request.session['post_count'] = post_count
            new_audio_file_name, new_audio_file_path = run_text_to_speech(response, post_count, now)
            
            # 현재 MP3 파일 경로를 세션에 저장
            request.session['audio_file_path'] = new_audio_file_path
            
            audio_url = '/static/' + new_audio_file_name
            print("audio_url:", audio_url)

            return JsonResponse({'response': response, 'audio_url': audio_url, 'history': request.session['history']})
        else:
            # 사용자 입력이 없는 경우, 경고 메시지와 함께 응답 반환
            return JsonResponse({'error': 'No user input provided'})
    elif request.method == 'GET':
        # GET 요청 시 대화 세션 초기화
        request.session['started'] = False
        request.session['history'] = []
        request.session['post_count'] = 0
        request.session['audio_file_path'] = None
    return render(request, 'query.html', {'history': request.session.get('history', [])})
