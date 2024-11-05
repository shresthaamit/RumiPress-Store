from django.shortcuts import render
from .serializers import UserRegisterSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
# Create your views here.
@api_view(["POST"],)
def user_registeration_view(request):
    if request.method == 'POST':
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            # return serializer.data
            return Response({"message": "User created successfully", "user_data": serializer.data},status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    