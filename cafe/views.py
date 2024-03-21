from django.shortcuts import render, redirect
from django.http import JsonResponse, FileResponse, HttpResponseNotFound
from django.contrib.auth import login as django_login
from django.conf import settings
import os, re
from datetime import datetime
import boto3
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import MenuSerializer
from google.cloud import texttospeech, speech

from pydub import AudioSegment
import openai

from .models import Menu
from .serializers import CafeOwnerRegisterSerializer, CustomLoginSerializer
class MenuListView(APIView):
    def get(self, request, *args, **kwargs):
        menus = Menu.objects.all()
        serializer = MenuSerializer(menus, many=True)
        return Response(serializer.data)
def upload_to_s3(file_name, file_content):
    s3_client = boto3.client(
        's3',
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_S3_REGION_NAME
    )
    file_path = f"audio/{file_name}"
    s3_client.put_object(Bucket=settings.AWS_STORAGE_BUCKET_NAME, Key=file_path, Body=file_content)
    file_url = f"https://{settings.AWS_STORAGE_BUCKET_NAME}.s3.{settings.AWS_S3_REGION_NAME}.amazonaws.com/audio/{file_name}"
    print("upload_to_s3 file_url: ",file_url)
    return file_url

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
        serializer = CafeOwnerRegisterSerializer(data=request.POST)
        if serializer.is_valid():
            serializer.save()
            # 회원가입 성공 시 사용자가 입력한 내용을 JSON으로 반환
            return JsonResponse({
                'name': serializer.validated_data.get('owner_name'),
                'email': serializer.validated_data.get('email'),
                'owner_phone_number': serializer.validated_data.get('owner_phone_number'),
                'cafe_name': serializer.validated_data.get('store_name'),
                'cafe_address': serializer.validated_data.get('store_address'),
                'cafe_phone_number': serializer.validated_data.get('store_phone_number')
            })
        # 유효성 검사 실패 시 에러 메시지를 포함한 JSON 반환
        return JsonResponse({'error_message': '유효하지 않은 회원가입 정보입니다.'}, status=400)
    else:
        return render(request, 'register.html')
    
def login(request):
    if request.method == 'POST':
        serializer = CustomLoginSerializer(data=request.POST)
        if serializer.is_valid():
            user = serializer.validated_data
            django_login(request, user)
            print("로그인성공")
            # 로그인에 성공한 경우 유저의 이메일을 JSON으로 반환
            return JsonResponse({
                'email': user.email,
                'name': user.owner_name
            })
        else:
            print("로그인실패")
            error_message = '유효하지 않은 로그인 정보입니다.'
            return JsonResponse({'error_message': error_message}, status=400)
    else:
        return render(request, 'login.html')


def home(request):
    return render(request, 'index.html')

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
                 # STT 작업이 완료된 후에 음성 데이터 파일을 삭제합니다.
                if os.path.exists(file_path):
                    os.remove(file_path)
                return Response({'status': 'success', 'transcripts': transcripts})
            except Exception as e:
                return Response({'status': 'error', 'message': str(e)})

        else:
            return Response({'status': 'error', 'message': 'No audio file provided'})

    return Response({'status': 'error', 'message': 'Invalid request method'})
# def transcribe_audio(request):
#     if request.method == 'POST':
#         # Audio recording parameters
#         RATE = 16000
#         CHUNK = int(RATE / 10)  # 100ms

#         # AWS S3 연결 설정
#         s3 = boto3.client('s3', aws_access_key_id='AWS_ACCESS_KEY_ID', aws_secret_access_key='AWS_SECRET_ACCESS_KEY')

#         # S3 버킷에서 가장 최근에 업로드된 객체 가져오기
#         bucket_name = 'AWS_STORAGE_BUCKET_NAME'
#         response = s3.list_objects_v2(Bucket=bucket_name)
#         latest_file = max(response['Contents'], key=lambda x: x['LastModified'])

#         # S3에서 파일 다운로드
#         file_path = os.path.join(settings.MEDIA_ROOT, 'audio', latest_file['Key'])
#         s3.download_file(bucket_name, latest_file['Key'], file_path)

#         # Google STT 클라이언트 생성
#         client = speech.SpeechClient()

#         # 파일 읽기
#         with open(file_path, "rb") as audio_file:
#             content = audio_file.read()

#         audio = speech.RecognitionAudio(content=content)
#         config = speech.RecognitionConfig(
#             encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
#             sample_rate_hertz=16000,
#             language_code="ko-KR",
#             enable_automatic_punctuation=True,
#         )

#         try:
#             # Google STT API 호출
#             response = client.recognize(config=config, audio=audio)
#             transcripts = [result.alternatives[0].transcript for result in response.results]
#             return JsonResponse({'status': 'success', 'transcripts': transcripts})
#         except Exception as e:
#             return JsonResponse({'status': 'error', 'message': str(e)})

#     return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

class TranscribeAudioView(APIView):
    def post(self, request, *args, **kwargs):
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
                 # STT 작업이 완료된 후에 음성 데이터 파일을 삭제합니다.
                if os.path.exists(file_path):
                    os.remove(file_path)
                return Response({'status': 'success', 'transcripts': transcripts})
            except Exception as e:
                return Response({'status': 'error', 'message': str(e)})

        else:
            return Response({'status': 'error', 'message': 'No audio file provided'})
class SpeechToTextView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        if 'audio' in request.FILES:
            audio_file = request.FILES['audio']
            audio_content = audio_file.read()

            client = speech.SpeechClient()
            audio = speech.RecognitionAudio(content=audio_content)
            config = speech.RecognitionConfig(
                encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
                sample_rate_hertz=16000,
                language_code="ko-KR",
                enable_automatic_punctuation=True,
            )

            try:
                response = client.recognize(config=config, audio=audio)
                transcripts = [result.alternatives[0].transcript for result in response.results]
                return Response({'status': 'success', 'transcripts': transcripts})
            except Exception as e:
                return Response({'status': 'error', 'message': str(e)})

        return Response({'status': 'error', 'message': 'No audio file provided'})
class QueryView(APIView):
    def get(self, request, *args, **kwargs):
        # GET 요청 처리 로직
        request.session['started'] = False
        request.session['history'] = []
        request.session['post_count'] = 0
        request.session['audio_file_path'] = None
        return Response({'message': '[GET 성공]Session reset successful'})

    def post(self, request, *args, **kwargs):
        user_input = request.data.get('response') #원래는 prompt이긴 했음. 
        print("request.data",request.data)
        print("user_input:",user_input)
        if user_input:
            print(user_input)
            response = self.get_completion(request, user_input)
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            print("302")
            post_count = request.session.get('post_count', 0) + 1
            request.session['post_count'] = post_count
            
            new_audio_web_url = self.run_text_to_speech(response, post_count, timestamp)
            print("new_audio_web_url:",new_audio_web_url)
            request.session['audio_file_path'] = new_audio_web_url
            print("response_message",response)
            return Response({"response": response, "audio_url": new_audio_web_url, "history": request.session['history']})
            
        else:
            return Response({'error': 'No user input provided'}, status=status.HTTP_400_BAD_REQUEST)

    def get_completion(self, request, user_input):
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
        print("[358] user:",user_input,"response:",response)
        request.session['history'].append({'user': user_input, 'bot': response})
        return response

    def run_text_to_speech(self, text, post_count, now):
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

        audio_url = upload_to_s3(output_file_name, open(output_file_path, "rb"))
        # 새로운 파일 이름과 경로를 반환
        return audio_url