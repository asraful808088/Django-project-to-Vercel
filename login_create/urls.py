from django.urls import path
from .views import CreateUsers,UserLogin,GetUserInfo,RefreshInfo
urlpatterns = [
    path('create/', CreateUsers.as_view()),
    path('login/', UserLogin.as_view()),
    path('getuser/', GetUserInfo.as_view()),
    path('refresh/', RefreshInfo.as_view()),
]
