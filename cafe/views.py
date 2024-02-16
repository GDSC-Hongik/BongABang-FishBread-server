from django.shortcuts import render, redirect
from django.http import JsonResponse, FileResponse, HttpResponseNotFound
from django.contrib.auth import login as django_login
from django.conf import settings
import os, re
from datetime import datetime

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from google.cloud import texttospeech, speech

from pydub import AudioSegment
import openai

from .models import Menu
from .serializers import CafeOwnerRegisterSerializer, CustomLoginSerializer

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
            
            ## Menu:
            할메가커피 , 0 , 1900 , 0 , onlyice / 왕할메가커피 , 0 , 2900 , 0 , onlyice / 아메리카노 , 1500 , 2000 , 0 , both / 메가리카노 , 0 , 3000 , 0 , onlyice / 꿀아메리카노 , 2700 , 2700 , 0 , both / 바닐라아메리카노 , 2700 , 2700 , 0 , both / 헤이즐넛아메리카노 , 2700 , 2700 , 0 , both / 카페라떼 , 2900 , 2900 , 0 , both / 카푸치노 , 2900 , 2900 , 0 , both / 바닐라라떼 , 3400 , 3400 , 0 , both / 헤이즐넛라떼 , 3400 , 3400 , 0 , both / 연유라떼 , 3900 , 0 , 0 , onlyhot / 카라멜마끼아또 , 3700 , 3700 , 0 , both / 카페모카 , 3900 , 3900 , 0 , both / 콜드브루오리지널 , 3500 , 3500 , 0 , both / 콜드브루라떼 , 4000 , 4000 , 0 , both / 티라미수라떼 , 3900 , 3900 , 0 , both / 큐브라떼 , 0 , 4200 , 0 , onlyice / 콜드브루디카페인 , 3500 , 3500 , 0 , both / 콜드브루디카페인라떼 , 4000 , 4000 , 0 , both / 딸기라떼 , 0 , 3700 , 0 , onlyice / 고구마라떼 , 3500 , 3500 , 0 , both / 곡물라떼 , 3300 , 3300 , 0 , both / 메가초코 , 3800 , 3800 , 0 , both / 토피넛라떼 , 3800 , 3800 , 0 , both / 오레오초코라떼 , 0 , 3900 , 0 , onlyice / 흑당버블밀크티라떼 , 0 , 3800 , 0 , onlyice / 흑당버블라떼 , 0 , 3700 , 0 , onlyice / 메가초코 , 3800 , 3800 , 0 , both / 녹차라떼 , 3500 , 3500 , 0 , both / 핫초코 , 3500 , 0 , 0 , onlyhot / 로얄밀크티라떼 , 3700 , 0 , 0 , onlyhot / 디카페인 아메리카노 , 2500 , 3000 , 0 , both / 디카페인 꿀아메리카노 , 3700 , 3700 , 0 , both / 디카페인 헤이즐넛 아메리카노 , 3700 , 3700 , 0 , both / 디카페인 바닐라 아메리카노 , 3700 , 3700 , 0 , both / 디카페인 카페라떼 , 3900 , 3900 , 0 , both / 디카페인 바닐라라떼 , 4400 , 4400 , 0 , both / 디카페인 연유라떼 , 4900 , 0 , 0 , onlyhot / 디카페인 카라멜마끼아또 , 4700 , 4700 , 0 , both / 디카페인 카페모카 , 4900 , 4900 , 0 , both / 디카페인 카푸치노 , 3900 , 3900 , 0 , both / 디카페인헤이즐넛라떼 , 4400 , 4400 , 0 , both / 디카페인티라미수라떼 , 4900 , 4900 , 0 , both / 디카페인 메가리카노 , 0 , 4500 , 0 , onlyice / 복숭아아이스티 , 0 , 3000 , 0 , onlyice / 허니자몽블랙티 , 3700 , 3700 , 0 , both / 사과유자차 , 3500 , 3500 , 0 , both / 유자차 , 3300 , 3300 , 0 , both / 레몬차 , 3300 , 3300 , 0 , both / 자몽차 , 3300 , 3300 , 0 , both / 녹차 , 2500 , 2500 , 0 , both / 페퍼민트 , 2500 , 2500 , 0 , both / 캐모마일 , 2500 , 2500 , 0 , both / 얼그레이 , 2500 , 2500 , 0 , both / 코코넛커피 스무디 , 0 , 0 , 4800 , no_temperature / 플레인퐁 크러쉬 , 0 , 0 , 3900 , no_temperature / 초코허니퐁 크러쉬 , 0 , 0 , 3900 , no_temperature / 슈크림허니 퐁크러쉬 , 0 , 0 , 3900 , no_temperature / 딸기퐁 크러쉬 , 0 , 0 , 3900 , no_temperature / 바나나퐁 크러쉬 , 0 , 0 , 3900 , no_temperature / 쿠키프라페 , 0 , 0 , 3900 , no_temperature / 딸기쿠키 프라페 , 0 , 0 , 3900 , no_temperature"""},
            {'role':'user','content': full_prompt}
        ], 
        max_tokens=1024, 
        n=1, 
        stop=None, 
        temperature=0.001, 
    ) 
    response = query.choices[0].message["content"]
    # 새 대화 내역 추가
    request.session['history'].append({'user': user_input, 'bot': response})
    return response

def run_text_to_speech(text, post_count,now):
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
