from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('api/', include("login_create.urls")),
    path('api/transection/', include("transection.urls")),
]
