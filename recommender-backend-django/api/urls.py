from django.urls import path
from rest_framework import routers
from django.conf.urls import include
from .views import UserViewSet, MovieViewSet, RatingViewSet, RecommenderViewSet

router = routers.DefaultRouter()
router.register('users', UserViewSet)
router.register('movies', MovieViewSet)
router.register('ratings', RatingViewSet)
router.register('recommender', RecommenderViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
