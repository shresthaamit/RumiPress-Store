from django.shortcuts import render
from .serializers import UserRegisterSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from django.contrib.auth import authenticate
# Create your views here.
@api_view(["POST"],)
def user_registeration_view(request):
    if request.method == 'POST':
        serializer = UserRegisterSerializer(data=request.data)
        data={}
        if serializer.is_valid():
            account = serializer.save()
            data['username'] = account.username
            data['email'] = account.email
            token = Token.objects.get(user=account).key
            data['token'] = token
            
            # return serializer.data
            return Response({"message": "User created successfully", "user_data": data},status=status.HTTP_201_CREATED)
        else:
            data = serializer.errors
        return Response(data)
        
     
@api_view(['POST'])
class custom_login(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        email  =  request.data.get('email')
        password =  request.data.get('password')
        user = authenticate(request,username=email, password=password)
        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
                'user_id': user.pk,
                'email': user.email
            }, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid email or password'}, status=status.HTTP_401_UNAUTHORIZED)
        
@api_view(['POST'])
def logout_view(request):
    if request.method == 'POST':
        try:
            request.user.auth_token.delete()
            return Response({"message": "User logged out successfully"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)