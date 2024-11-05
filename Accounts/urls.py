from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from .views import *
urlpatterns = [
    path('register/', user_registeration_view, name='register'),
    path('login/', obtain_auth_token, name="login")

    
]