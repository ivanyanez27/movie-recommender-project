from django.urls import path
from rest_framework import routers
from django.conf.urls import include
from .views import MovieViewSet, RatingViewSet, UserViewSet, LinkViewSet

router = routers.DefaultRouter()
router.register('users', UserViewSet)
router.register('movies', MovieViewSet)
router.register('ratings', RatingViewSet)
router.register('link', LinkViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
