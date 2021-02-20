from . import views
from .views import UserFunction
from django.urls import path, include

urlpatterns = [
    path('test', views.test),
    #path('userf', UserFunction.as_view())
]
