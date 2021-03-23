import sys
from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from .views import CustomObtainAuthToken

urlpatterns = [
    path('grappelli/', include('grappelli.urls')),
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('auth/', CustomObtainAuthToken.as_view()),
]
