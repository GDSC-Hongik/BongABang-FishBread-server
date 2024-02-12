import openai
import json
import io
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import ValidationError
from google.cloud import texttospeech
from google.cloud.speech_v1 import types
from django.http import JsonResponse, FileResponse,HttpResponseNotFound
from django.contrib.auth import login as django_login, authenticate
from django.shortcuts import render,redirect
from google.protobuf.json_format import MessageToDict
from google.cloud import speech
from datetime import datetime
from pydub import AudioSegment
import base64
from django.views import View
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

def query_view(request): 
	if request.method == 'POST': 
		prompt = request.POST.get('prompt') 
		prompt=str(prompt)
		response = get_completion(prompt)
		return JsonResponse({'response': response}) 
	return render(request, 'query.html') 
def RealTimeSTT(request):
    return render(request,'stt.html')

def convert_sample_rate(input_file, target_sample_rate):
    sound = AudioSegment.from_file(input_file)
    sound = sound.set_frame_rate(target_sample_rate) # 샘플레이트 변경하기
    sound = sound.set_sample_width(2)  # 2바이트(16비트) 샘플로 설정
    sound.export(input_file, format="wav")

def transcribe_audio(request):
    if request.method == 'POST':
        # Audio recording parameters
        RATE = 16000
        CHUNK = int(RATE / 10)  # 100ms

        if 'audio' in request.FILES:
            # 음성 데이터 가져오기
            audio_file = request.FILES['audio']

            # 로컬 디렉터리에 저장 (media/audio/ 하위에 저장됨)
            # 현재 시간을 기반으로 파일 이름 생성
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            file_name = f"inputaudio_{timestamp}.wav"
            file_path = os.path.join(settings.MEDIA_ROOT, 'audio', file_name)
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            # 음성 데이터 저장하기
            with open(file_path, 'wb') as destination:
                for chunk in audio_file.chunks():
                    destination.write(chunk)

            # Convert the sample rate of the audio file to 16kHz
            convert_sample_rate(file_path, RATE)
            
            client = speech.SpeechClient()
            
            with open(file_path, "rb") as audio_file_2:
                content = audio_file_2.read()

            audio = speech.RecognitionAudio(content=content)
            config = speech.RecognitionConfig(
                encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
                sample_rate_hertz=16000,
                language_code="ko-KR",
                enable_automatic_punctuation=True,
            )

            try:
                response = client.recognize(config=config, audio=audio)
                transcripts = [result.alternatives[0].transcript for result in response.results]
                return JsonResponse({'status': 'success', 'transcripts': transcripts})
            except Exception as e:
                return JsonResponse({'status': 'error', 'message': str(e)})

        else:
            return JsonResponse({'status': 'error', 'message': 'No audio file provided'})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})
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
            {'role':'system','content': """
             You're a friendly, hardworking, flexible employee at a cafe in Korea.
             When making menu recommendations, give fewer than four suggestions, and then add one of your favorites.
             So, You must speak only in Korean  
            <When a customer greets you>
            Greet them kindly and invite them to place an order. 

            <Ordering rules>
            Kindly take the customer's order.
            When taking an order, be sure to check the temperature options and quantity information for each item.
            If you're not sure what to order, consider the description on the menu board and make short and impactful menu recommendations.
            And when you're sure that you've chosen the right menu, you should ask the customer if they want to add the menu to their order.

            <Temperature options>
            When the customer selects a menu, you need to check the price of that menu and ask for the temperature option. 
            If the menu_type is 'onlyice', only cold drinks are available, and if it is 'both', both cold and hot drinks are available, so we need to ask them to select an option,
            If it's 'onlyhot', it's only hot drinks, and if it's 'no_temperature', there's no temperature option, so we shouldn't ask for it.
            
            <Menu>
            [{'할메가커피'}, {'왕할메가커피'}, {'아메리카노'}, {'메가리카노'}, {'꿀아메리카노'}, {'바닐라아메리카노'}, {'헤이즐넛아메리카노'}, {'카페라떼'}, {'카푸치노'}, {'바닐라라떼'}, {'헤이즐넛라떼'}, {'연유라떼'}, {'카라멜마끼아또'}, {'카페모카'}, {'콜드브루오리지널'}, {'콜드브루라떼'}, {'티라미수라떼'}, {'큐브라떼'}, {'콜드브루디카페인'}, {'콜드브루디카페인라떼'}, {'딸기라떼'}, {'고구마라떼'}, {'곡물라떼'}, {'메가초코'}, {'토피넛라떼'}, {'오레오초코라떼'}, {'흑당버블밀크티라떼'}, {'흑당버블라떼'}, {'메가초코'}, {'녹차라떼'}, {'핫초코'}, {'로얄밀크티라떼'}, {'디카페인 아메리카노'}, {'디카페인 꿀아메리카노'}, {'디카페인 헤이즐넛 아메리카노'}, {'디카페인 바닐라 아메리카노'}, {'디카페인 카페라떼'}, {'디카페인 바닐라라떼'}, {'디카페인 연유라떼'}, {'디카페인 카라멜마끼아또'}, {'디카페인 카페모카'}, {'디카페인 카푸치노'}, {'디카페인헤이즐넛라떼'}, {'디카페인티라미수라떼'}, {'디카페인 메가리카노'}, {'화이트 뱅쇼'}, {'복숭아아이스티'}, {'허니자몽블랙티'}, {'사과유자차'}, {'유자차'}, {'레몬차'}, {'자몽차'}, {'녹차'}, {'페퍼민트'}, {'캐모마일'}, {'얼그레이'}, {'스모어 블랙쿠키 프라페'}, {'스모어 카라멜쿠키 프라페'}, {'코코넛커피 스무디'}, {'플레인퐁 크러쉬'}, {'초코허니퐁 크러쉬'}, {'슈크림허니 퐁크러쉬'}, {'딸기퐁 크러쉬'}, {'바나나퐁 크러쉬'}, {'쿠키프라페'}, {'딸기쿠키 프라페'}, {'민트프라페'}, {'커피프라페'}, {'리얼초코프라페'}, {'녹차프라페'}, {'스트로베리 치즈홀릭'}, {'플레인요거트 스무디'}, {'딸기요거트 스무디'}, {'망고요거트 스무디'}, {'스노우 샹그리아 에이드'}, {'레드오렌지 자몽주스'}, {'샤인머스캣 그린주스'}, {'딸기주스'}, {'딸기바나나 주스'}, {'메가에이드'}, {'레몬에이드'}, {'블루레몬 에이드'}, {'자몽에이드'}, {'청포도에이드'}, {'유니콘매직에이드 (핑크)'}, {'유니콘매직에이드 (블루)'}, {'체리콕'}, {'라임모히또'}, {'따끈따끈 간식꾸러미'}, {'초코스모어 쿠키'}, {'뚱크림치즈약과쿠키'}, {'와앙 피자 보름달빵'}, {'와앙 콘마요 보름달빵'}, {'오트밀 팬케이크'}, {'티라미수 팬케이크'}, {'그래놀라 스모어쿠키'}, {'크로크무슈'}, {'버터버터소금빵'}, {'햄앤치즈샌드'}, {'아이스허니 와앙슈'}, {'몽쉘케이크'}, {'말차스모어 쿠키'}, {'플레인크로플'}, {'아이스크림 크로플'}, {'머그(옐로우)'}, {'메가엠지씨스틱 오리지날 아메리카노'}, {'메가엠지씨스틱 디카페인 아메리카노'}, {'메가엠지씨스틱 스테비아 믹스커피'}, {'메가 엠지씨 스틱 스테비아 디카페인 믹스커피'}, {'스테비아 케이스'}, {'메가 엠지씨 티플레저 블루밍 캐모마일'}, {'메가 엠지씨 티플레저 프루티 루이보스'}, {'메가 엠지씨 티플레저 스위트 히비스커스'}, {'MGC 텀블러(웜그레이)'}, {'MGC 텀블러(옐로우)'}, {'MGC 텀블러(스카이)'}, {'텀블러(실버)'}, {'텀블러(브론즈)'}, {'텀블러(화이트)'}]
            
            """},
            {'role':'user','content': "너가 계속해서 내 이전 대화와 현재 대화를 듣고 주문을 받아줘"},
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
    # os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="/Users/jeonjisu/Desktop/university/project/BongABang-FishBread-server/codebook/bong-a-bang-412508-9e4d0ff505ce.json"
    client = texttospeech.TextToSpeechClient()
    synthesis_input = texttospeech.SynthesisInput(text=text)
    voice = texttospeech.VoiceSelectionParams(
        language_code="ko-KR", ssml_gender=texttospeech.SsmlVoiceGender.FEMALE
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )
    
    # 새로운 파일 이름 생성
    output_file_name = f"newoutput_v{post_count}_{now}.mp3"
    output_file_path = os.path.join(settings.MEDIA_ROOT, output_file_name)
    print("output_file_path 저장위치:",output_file_path)
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
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

            # 새로운 파일 이름을 얻어옴
            post_count = request.session.get('post_count', 0)
            post_count += 1
            request.session['post_count'] = post_count
            new_audio_file_name, new_audio_file_path = run_text_to_speech(response, post_count, timestamp)
            
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
