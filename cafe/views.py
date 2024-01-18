# # views.py

# from rest_framework.response import Response
# from rest_framework.authtoken.models import Token
# from .serializers import LoginSerializer

# class CustomLoginView():
#     serializer_class = LoginSerializer

#     def post(self, request, *args, **kwargs):
#         serializer = self.serializer_class(data=request.data, context={'request': request})
#         serializer.is_valid(raise_exception=True)
#         user = serializer.validated_data['user']
#         token, created = Token.objects.get_or_create(user=user)
#         return Response({'token': token.key})
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import ValidationError
from .serializers import CustomLoginSerializer

class CustomLoginView(APIView):
    serializer_class = CustomLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        try:
            if serializer.is_valid(raise_exception=True):
                user = serializer.validated_data['user']
                refresh = RefreshToken.for_user(user)
                return Response({
                    'access_token': str(refresh.access_token),
                    'refresh_token': str(refresh),
                }, status=status.HTTP_200_OK)
        except ValidationError as e:
            return Response(e.detail, status=status.HTTP_400_BAD_REQUEST)
