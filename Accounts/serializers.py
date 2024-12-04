from rest_framework import serializers
from django.contrib.auth.models import User
from .models import CustomUser
from datetime import date
from django.contrib.auth import get_user_model
class UserRegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'},write_only=True)
    registration_date = serializers.SerializerMethodField()
    
    class Meta:
        model=User
        fields=['username','email','password','password2','registration_date']
        extra_kwargs={
            'password':{'write_only':True}
        }
        
    def get_registration_date(self, obj):
        return date.today()
        
    def save(self,**kwargs):
        password = self.validated_data['password']
        password2 = self.validated_data['password2']
        
        if password != password2:
            raise serializers.ValidationError({'error':'password doesnot match '})
        
        if User.objects.filter(email= self.validated_data['email']).exists():
            raise serializers.ValidationError({'error':'email already exists'})
        
        account  = User(email =self.validated_data['email'] , username = self.validated_data['username'])
        account.set_password(password)
        account.save()
        return account     
    
    
