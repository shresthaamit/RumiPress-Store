from django.shortcuts import render
from .serializers import UserRegisterSerializer,UserProfileSerializer
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from .serializers import UserProfileSerializer
from .models import CustomUser,UserProfile
from rest_framework import generics, permissions
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from rest_framework.request import Request 
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
        
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def check_user_status(request):
    """
    Returns the login status and details of the authenticated user,
    including profile information.
    """
    if request.user.is_authenticated:
        try:
            # Retrieve the user's profile
            user_profile = UserProfile.objects.get(user=request.user)
            profile_picture_url = user_profile.profile_picture.url if user_profile.profile_picture else None
        except UserProfile.DoesNotExist:
            # Handle case where the profile does not exist
            profile_picture_url = None

        # If the user is logged in, return user details
        return Response({
            "status": "Logged In",
            "detail": {
                "username": request.user.username,
                "email": request.user.email,
                "date_joined": request.user.date_joined.strftime("%Y-%m-%d"),
                "profile_picture": profile_picture_url
            }
        }, status=status.HTTP_200_OK)
    else:
        # If the user is not logged in, return anonymous status
        return Response({
            "status": "Not Logged In",
            "detail": "Anonymous User",
        }, status=status.HTTP_401_UNAUTHORIZED)
        
class UserProfileView(generics.RetrieveUpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get_object(self):
        return self.request.user
# views.py@api_view(['PUT'])
# @csrf_exempt  # Disable CSRF protection for this view (if needed)@api_view(['PUT'])
# @api_view(['PUT'])
# @permission_classes([IsAuthenticated])
# def update_profile(request):
#     user_profile, created = UserProfile.objects.get_or_create(user=request.user)

#     serializer = UserProfileSerializer(user_profile, data=request.data, partial=True)

#     if serializer.is_valid():
#         updated_profile = serializer.save()
#         profile_picture_url = updated_profile.profile_picture.url if updated_profile.profile_picture else None

#         return Response({
#             "message": "Profile updated successfully", 
#             "profile_picture": profile_picture_url
#         }, status=status.HTTP_200_OK)

#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class UserProfileView(generics.RetrieveUpdateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get_object(self):
        # Get or create the user's profile
        user_profile, created = UserProfile.objects.get_or_create(user=self.request.user)
        return user_profile

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', True)  # Allow partial updates
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        
        if serializer.is_valid():
            updated_profile = serializer.save()
            print(updated_profile)
            # Get the profile picture URL after saving
            profile_picture_url = updated_profile.profile_picture.url if updated_profile.profile_picture else None
            updated_user = updated_profile.user
            return Response({
            "message": "Profile updated successfully",
            "username": updated_user.username,
            "email": updated_user.email,
            "profile_picture": profile_picture_url
        }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
