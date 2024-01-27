from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import ValidationError
from django.http import JsonResponse
from django.contrib.auth import login as django_login, authenticate
from django.shortcuts import render,redirect
import openai
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

# views.py
def get_completion2(request, user_input): 
    # 대화 세션 시작 체크
    
    if True:
        # 텍스트 파일에서 프롬프트 읽기
        with open('/Users/jeonjisu/Desktop/대학/프로젝트/BongABang-FishBread-server/cafe/prompt.txt', 'r', encoding='utf-8') as file:
            fixed_prompt = file.read()
            print(fixed_prompt)
        full_prompt = fixed_prompt + "\n\n" + user_input
        request.session['started'] = True
    else:
        full_prompt = user_input

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
    
    # 대화 내역 세션에 저장
    if 'history' not in request.session:
        request.session['history'] = []
    request.session['history'].append({'user': user_input, 'bot': response})
    
    return response

def query_view2(request): 
    if request.method == 'POST': 
        user_input = request.POST.get('prompt') 
        user_input = str(user_input)
        response = get_completion2(request, user_input)
        return JsonResponse({'response': response, 'history': request.session['history']}) 
    elif request.method == 'GET':
        # GET 요청 시 대화 세션 초기화
        request.session['started'] = False
        request.session['history'] = []
    return render(request, 'query.html', {'history': request.session.get('history', [])}) 
