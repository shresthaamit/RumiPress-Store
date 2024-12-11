from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from .views import *
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('register/', user_registeration_view, name='register'),
    # path('login/', obtain_auth_token, name="login")
    path("login/",obtain_auth_token, name="login"),
    #  path("login/", CustomLogin.as_view(), name="login"),
    path('logout/',logout_view, name="logout"),
    path('checkstatus/', check_user_status, name='check-status'),
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('update_profile/', update_profile, name='update_profile'),
    
]