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
    
    
class UserProfileSerializer(serializers.ModelSerializer):
    profile_picture = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = CustomUser  
        fields = ['username', 'email', 'profile_picture']
        extra_kwargs = {
            'email': {'required': False},
            'username': {'required': False},
        }

    def update(self, instance, validated_data):
        profile_picture = validated_data.pop('profile_picture', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if profile_picture:
            instance.profile_picture = profile_picture
        instance.save()
        return instance