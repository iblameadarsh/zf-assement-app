from django.urls import path, include
from authentication.views import UserRegisterView, UserLoginView, UserRetrieveView

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='register_user'),
    path('login/', UserLoginView.as_view(), name='user_login'),
    path('get-user/', UserRetrieveView.as_view(), name='user')
    
]
