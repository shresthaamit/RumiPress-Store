from rest_framework import serializers
from django.contrib.auth.models import User
from .models import CustomUser,UserProfile
from datetime import date
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework.exceptions import ValidationError
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
    
# class UserProfileSerializer(serializers.ModelSerializer):
#     profile_picture = serializers.ImageField(required=False, allow_null=True)
#     password = serializers.CharField(write_only=True, required=False)
#     confirm_password = serializers.CharField(write_only=True, required=False)

#     class Meta:
#         model = CustomUser
#         fields = ['username', 'email', 'profile_picture', 'password', 'confirm_password']
#         extra_kwargs = {
#             'email': {'required': False},
#             'username': {'required': False},
#         }

#     def validate(self, data):
#         password = data.get('password')
#         confirm_password = data.get('confirm_password')

#         if password and confirm_password:
#             if password != confirm_password:
#                 raise ValidationError({"password": "Passwords do not match."})
#             validate_password(password)  # Validates the password using Django's built-in validators
#         return data

#     def update(self, instance, validated_data):
#         # Handle profile_picture update only if provided
#         profile_picture = validated_data.pop('profile_picture', None)
#         for attr, value in validated_data.items():
#             setattr(instance, attr, value)

#         if profile_picture is not None:  # Only update if a new picture is provided
#             instance.profile_picture = profile_picture

#         password = validated_data.pop('password', None)
#         validated_data.pop('confirm_password', None)
#         if password:
#             instance.set_password(password)

#         instance.save()
#         return instance


# class UserProfileSerializer(serializers.ModelSerializer):
#     profile_picture = serializers.ImageField(required=False, allow_null=True)

#     class Meta:
#         model = UserProfile
#         fields = ['profile_picture']

#     def update(self, instance, validated_data):
#         profile_picture = validated_data.pop('profile_picture', None)

#         if profile_picture is not None:
#             instance.profile_picture = profile_picture

#         instance.save()
#         return instance
class UserProfileSerializer(serializers.ModelSerializer):
    profile_picture = serializers.ImageField(required=False, allow_null=True)
    username = serializers.CharField(required=False)
    email = serializers.EmailField(required=False)
    password = serializers.CharField(write_only=True, required=False)
    confirm_password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'profile_picture', 'password', 'confirm_password']
        extra_kwargs = {
            'email': {'required': False},
            'username': {'required': False},
        }

    def validate(self, data):
        password = data.get('password')
        confirm_password = data.get('confirm_password')

        # Validate passwords match
        if password and confirm_password:
            if password != confirm_password:
                raise serializers.ValidationError({"password": "Passwords do not match."})
            try:
                validate_password(password)  # Validate the password
            except ValidationError as e:
                raise serializers.ValidationError({"password": list(e.messages)})

        return data

    def update(self, instance, validated_data):
    # Update the profile picture
        profile_picture = validated_data.pop('profile_picture', None)
        if profile_picture is not None:
            instance.profile_picture = profile_picture

        # Access related user model
        user = instance.user

        # Update username and email if provided
        username = validated_data.get('username')
        if username:
            user.username = username

        email = validated_data.get('email')
        if email:
            user.email = email

        # Update password if provided
        password = validated_data.pop('password', None)
        validated_data.pop('confirm_password', None)  # Remove confirm_password as it's not a model field
        if password:
            user.set_password(password)

        # Save the updated user instance
        user.save()

        # Save the updated profile instance
        instance.save()
        return instance